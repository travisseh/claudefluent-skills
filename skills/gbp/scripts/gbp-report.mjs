#!/usr/bin/env node

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createRequire } from 'node:module'

const DEFAULT_DASHBOARD_DIR = '/Users/you/Programming/example-company-reporting/apps/dashboard'

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return
  const text = fs.readFileSync(filePath, 'utf8')
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (!line || line.startsWith('#') || !line.includes('=')) continue
    const [key, ...rest] = line.split('=')
    if (process.env[key]) continue
    let value = rest.join('=').trim()
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1)
    }
    process.env[key] = value
  }
}

function findDashboardDir() {
  const cwd = process.cwd()
  const candidates = [
    cwd,
    path.join(cwd, 'apps/dashboard'),
    DEFAULT_DASHBOARD_DIR,
  ]
  return candidates.find(candidate => fs.existsSync(path.join(candidate, '.env.local'))) ?? DEFAULT_DASHBOARD_DIR
}

const dashboardDir = findDashboardDir()
loadEnvFile(path.join(dashboardDir, '.env.local'))

function requireEnv(name) {
  const value = process.env[name]
  if (!value) throw new Error(`Missing ${name}. Expected it in ${path.join(dashboardDir, '.env.local')}`)
  return value
}

async function getAccessToken() {
  const response = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: requireEnv('GOOGLE_OAUTH_CLIENT_ID'),
      client_secret: requireEnv('GOOGLE_OAUTH_CLIENT_SECRET'),
      refresh_token: requireEnv('GBP_REFRESH_TOKEN'),
      grant_type: 'refresh_token',
    }),
  })

  const text = await response.text()
  if (!response.ok) throw new Error(`GBP token refresh failed: ${response.status} ${text}`)
  return JSON.parse(text).access_token
}

async function fetchJson(url, token) {
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  })
  const text = await response.text()
  if (!response.ok) throw new Error(`GBP API error ${response.status} for ${url}: ${text}`)
  return JSON.parse(text)
}

async function listAccounts(token) {
  const accounts = []
  let pageToken
  do {
    const url = new URL('https://mybusinessaccountmanagement.googleapis.com/v1/accounts')
    url.searchParams.set('pageSize', '100')
    if (pageToken) url.searchParams.set('pageToken', pageToken)
    const data = await fetchJson(url, token)
    accounts.push(...(data.accounts ?? []))
    pageToken = data.nextPageToken
  } while (pageToken)
  return accounts
}

function compactLocation(account, location) {
  return {
    accountName: account.accountName ?? account.name,
    accountResource: account.name,
    resourceName: location.name,
    title: location.title ?? '',
    placeId: location.metadata?.placeId ?? null,
    mapsUri: location.metadata?.mapsUri ?? null,
    newReviewUri: location.metadata?.newReviewUri ?? null,
    address: location.storefrontAddress ?? null,
    phone: location.phoneNumbers?.primaryPhone ?? null,
    websiteUri: location.websiteUri ?? null,
    primaryCategory: location.categories?.primaryCategory?.displayName ?? null,
    openStatus: location.openInfo?.status ?? null,
    hasVoiceOfMerchant: location.metadata?.hasVoiceOfMerchant ?? null,
  }
}

async function listGbpLocations() {
  const token = await getAccessToken()
  const accounts = await listAccounts(token)
  const locations = []

  for (const account of accounts) {
    let pageToken
    do {
      const url = new URL(`https://mybusinessbusinessinformation.googleapis.com/v1/${account.name}/locations`)
      url.searchParams.set('pageSize', '100')
      url.searchParams.set('readMask', 'name,title,metadata,storefrontAddress,phoneNumbers,websiteUri,categories,openInfo')
      if (pageToken) url.searchParams.set('pageToken', pageToken)
      const data = await fetchJson(url, token)
      for (const location of data.locations ?? []) {
        locations.push(compactLocation(account, location))
      }
      pageToken = data.nextPageToken
    } while (pageToken)
  }

  return { accounts, locations }
}

function normalize(value) {
  return String(value ?? '').toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, ' ').trim()
}

async function queryProductLocations(search) {
  requireEnv('DATABASE_URL')
  const require = createRequire(fileURLToPath(import.meta.url))
  const { Pool } = require(path.join(dashboardDir, 'node_modules/pg'))
  const dbUrl = new URL(process.env.DATABASE_URL)
  dbUrl.searchParams.delete('sslmode')
  const pool = new Pool({
    connectionString: dbUrl.toString(),
    ssl: { rejectUnauthorized: false },
    max: 2,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 10000,
  })
  try {
    const pattern = `%${search.toLowerCase()}%`
    const result = await pool.query(
      `
        SELECT
          l.id,
          l.name AS location_name,
          l.google_place_id,
          l.status,
          a.id AS account_id,
          a.name AS account_name
        FROM locations l
        JOIN accounts a ON a.id = l.account_id
        WHERE lower(l.name) LIKE $1
           OR lower(a.name) LIKE $1
        ORDER BY a.name, l.name
      `,
      [pattern]
    )
    return result.rows
  } finally {
    await pool.end()
  }
}

async function main() {
  const [command, ...args] = process.argv.slice(2)
  const query = args.join(' ').trim()

  if (!command || command === 'help') {
    console.log(`Usage:
  gbp-report.mjs summary
  gbp-report.mjs search <name>
  gbp-report.mjs search-place <google_place_id>
  gbp-report.mjs product-search <name>
  gbp-report.mjs product-gbp-check <name>`)
    return
  }

  if (command === 'product-search') {
    console.log(JSON.stringify(await queryProductLocations(query), null, 2))
    return
  }

  const { accounts, locations } = await listGbpLocations()

  if (command === 'summary') {
    console.log(JSON.stringify({
      accountCount: accounts.length,
      locationCount: locations.length,
      accounts: accounts.map(account => ({
        name: account.name,
        accountName: account.accountName ?? null,
        type: account.type ?? null,
      })),
    }, null, 2))
    return
  }

  if (command === 'search') {
    const needle = normalize(query)
    console.log(JSON.stringify(locations.filter(location => normalize(location.title).includes(needle)), null, 2))
    return
  }

  if (command === 'search-place') {
    console.log(JSON.stringify(locations.filter(location => location.placeId === query), null, 2))
    return
  }

  if (command === 'product-gbp-check') {
    const productLocations = await queryProductLocations(query)
    const gbpByPlaceId = new Map(locations.filter(location => location.placeId).map(location => [location.placeId, location]))
    console.log(JSON.stringify(productLocations.map(location => ({
      ...location,
      gbpManaged: Boolean(location.google_place_id && gbpByPlaceId.has(location.google_place_id)),
      gbpLocation: location.google_place_id ? gbpByPlaceId.get(location.google_place_id) ?? null : null,
    })), null, 2))
    return
  }

  throw new Error(`Unknown command: ${command}`)
}

main().catch(error => {
  console.error(error.message)
  process.exit(1)
})
