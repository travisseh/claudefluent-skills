#!/usr/bin/env tsx
import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

type Section = 'all' | 'product' | 'campaigns'
type OutputFormat = 'summary' | 'json'

type CliOptions = {
  section: Section
  format: OutputFormat
  days: number
  startDate?: string
  endDate?: string
  csmId?: string
  accountId?: string
  groupByLocation: boolean
  usePrimary: boolean
  dbUrlEnv?: string
  out?: string
}

const DASHBOARD_DIR = '/Users/you/Programming/example-company-reporting/apps/dashboard'
const READONLY_DATABASE_ENV_KEYS = [
  'BOOSTLY_REPORTING_READONLY_DATABASE_URL',
  'READONLY_DATABASE_URL',
  'V2_READ_REPLICA_DATABASE_URL',
  'V2_READONLY_DATABASE_URL',
  'V2_DATABASE_URL',
  'DATABASE_READONLY_URL',
  'REPLICA_DATABASE_URL',
]

function parseArgs(argv: string[]): CliOptions {
  const options: CliOptions = {
    section: 'all',
    format: 'summary',
    days: 14,
    groupByLocation: false,
    usePrimary: false,
  }

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i]
    const next = argv[i + 1]
    if (arg === '--section' && next) {
      if (!['all', 'product', 'campaigns'].includes(next)) throw new Error(`Invalid --section ${next}`)
      options.section = next as Section
      i++
    } else if (arg === '--format' && next) {
      if (!['summary', 'json'].includes(next)) throw new Error(`Invalid --format ${next}`)
      options.format = next as OutputFormat
      i++
    } else if (arg === '--days' && next) {
      options.days = Number.parseInt(next, 10)
      if (!Number.isFinite(options.days) || options.days < 1) throw new Error('--days must be a positive integer')
      i++
    } else if (arg === '--start-date' && next) {
      options.startDate = next
      i++
    } else if (arg === '--end-date' && next) {
      options.endDate = next
      i++
    } else if (arg === '--csm-id' && next) {
      options.csmId = next
      i++
    } else if (arg === '--account-id' && next) {
      options.accountId = next
      i++
    } else if (arg === '--group-by-location') {
      options.groupByLocation = true
    } else if (arg === '--use-primary') {
      options.usePrimary = true
    } else if (arg === '--db-url-env' && next) {
      options.dbUrlEnv = next
      i++
    } else if (arg === '--out' && next) {
      options.out = next
      i++
    } else if (arg === '--help' || arg === '-h') {
      printHelp()
      process.exit(0)
    }
  }

  return options
}

function printHelp() {
  console.log(`Usage:
  dashboard-stats.ts [--section all|product|campaigns] [--format summary|json]

Options:
  --days <n>              Transcript segment window. Default: 14
  --start-date YYYY-MM-DD Campaigns start date. Default: 7 days ago
  --end-date YYYY-MM-DD   Campaigns end date. Default: today
  --csm-id <id>           Campaigns support filter
  --account-id <id>       Campaigns account filter
  --group-by-location     Campaigns location grouping
  --db-url-env <name>      Use a specific env var as DATABASE_URL
  --use-primary           Keep the configured primary DATABASE_URL
  --out <path>            Write full JSON to file
`)
}

function moduleUrl(relativePath: string) {
  return pathToFileURL(path.join(DASHBOARD_DIR, relativePath)).href
}

function isoDateDaysAgo(daysAgo: number) {
  const date = new Date()
  date.setDate(date.getDate() - daysAgo)
  return date.toISOString().slice(0, 10)
}

function todayIsoDate() {
  return new Date().toISOString().slice(0, 10)
}

function loadEnvFile(filePath: string) {
  if (!fs.existsSync(filePath)) return

  const content = fs.readFileSync(filePath, 'utf8')
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (!line || line.startsWith('#')) continue
    const equalsIndex = line.indexOf('=')
    if (equalsIndex === -1) continue

    const key = line.slice(0, equalsIndex).trim()
    let value = line.slice(equalsIndex + 1).trim()
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1)
    }
    if (!process.env[key]) process.env[key] = value
  }
}

function findReadonlyDatabaseUrl() {
  for (const key of READONLY_DATABASE_ENV_KEYS) {
    const value = process.env[key]
    if (value) return { key, value }
  }
  return null
}

function safeDatabaseHost(urlValue: string | undefined) {
  if (!urlValue) return null
  try {
    const url = new URL(urlValue)
    return `${url.hostname}${url.port ? `:${url.port}` : ''}`
  } catch {
    return 'unparseable-url'
  }
}

function configureDatabaseForQueries(options: CliOptions) {
  const originalDatabaseUrl = process.env.DATABASE_URL
  const originalSalesDatabaseUrl = process.env.SALES_DATABASE_URL

  if (options.dbUrlEnv) {
    const selectedUrl = process.env[options.dbUrlEnv]
    if (!selectedUrl) {
      return {
        mode: 'missing-selected-env',
        sourceEnv: options.dbUrlEnv,
        host: null,
        warning: `Requested --db-url-env ${options.dbUrlEnv}, but it is not set.`,
      }
    }

    process.env.DATABASE_URL = selectedUrl
    process.env.SALES_DATABASE_URL = selectedUrl
    return {
      mode: 'selected-env',
      sourceEnv: options.dbUrlEnv,
      host: safeDatabaseHost(selectedUrl),
    }
  }

  if (options.usePrimary) {
    return {
      mode: 'primary',
      sourceEnv: 'DATABASE_URL',
      host: safeDatabaseHost(originalDatabaseUrl),
    }
  }

  const readonly = findReadonlyDatabaseUrl()
  if (readonly) {
    process.env.DATABASE_URL = readonly.value
    process.env.SALES_DATABASE_URL = readonly.value
    return {
      mode: 'read-replica',
      sourceEnv: readonly.key,
      host: safeDatabaseHost(readonly.value),
    }
  }

  return {
    mode: 'configured',
    sourceEnv: originalSalesDatabaseUrl ? 'SALES_DATABASE_URL/DATABASE_URL' : 'DATABASE_URL',
    host: safeDatabaseHost(originalSalesDatabaseUrl ?? originalDatabaseUrl),
    warning: 'No read-only database URL env var was found; using the configured database URL.',
  }
}

async function safe<T>(label: string, promise: Promise<T>): Promise<T | { error: string }> {
  try {
    return await promise
  } catch (error) {
    return { error: `${label} failed: ${error instanceof Error ? error.message : String(error)}` }
  }
}

async function loadProductStats(options: CliOptions) {
  const [
    productDb,
    productHubspot,
    productSheets,
    productSeo,
    productMeta,
    salesQueries,
    salesAnalysis,
  ] = await Promise.all([
    import(moduleUrl('src/lib/product-db.ts')),
    import(moduleUrl('src/lib/product-hubspot.ts')),
    import(moduleUrl('src/lib/product-sheets.ts')),
    import(moduleUrl('src/lib/product-seo.ts')),
    import(moduleUrl('src/lib/product-meta.ts')),
    import(moduleUrl('src/lib/sales-queries.ts')),
    import(moduleUrl('src/lib/sales-analysis.ts')),
  ])

  const fulfillment = await safe('fulfillment', productHubspot.getFulfillmentData())

  const [overview, costData, seoData, marketing, journey, inbound, sdr, sales, activation, csm] =
    await Promise.all([
      safe('product overview', productDb.getDashboardData()),
      safe('box economics', productSheets.getCostData()),
      safe('seo', 'error' in fulfillment ? Promise.resolve(null) : productSeo.getSeoData(fulfillment)),
      safe('marketing', productMeta.getMetaMarketingData()),
      safe('customer journey', salesAnalysis.getCustomerJourneyInsight()),
      safe('inbound', salesQueries.getTranscriptSegmentDashboardData('inbound', options.days)),
      safe('sdr', salesQueries.getTranscriptSegmentDashboardData('sdr', options.days)),
      safe('sales', salesQueries.getTranscriptSegmentDashboardData('sales', options.days)),
      safe('activation', salesQueries.getTranscriptSegmentDashboardData('activation', options.days)),
      safe('csm', salesQueries.getTranscriptSegmentDashboardData('csm', options.days)),
    ])

  return {
    overview,
    fulfillment,
    costData,
    seoData,
    marketing,
    journey,
    transcripts: { inbound, sdr, sales, activation, csm },
  }
}

async function loadCampaignStats(options: CliOptions) {
  const queries = await import(moduleUrl('src/lib/queries.ts'))
  const startDate = options.startDate ?? isoDateDaysAgo(7)
  const endDate = options.endDate ?? todayIsoDate()

  const [
    filters,
    typeData,
    nameData,
    typeTotals,
    nameTotals,
    engagementMetrics,
    promotionNames,
    subscriberTimeline,
    contactActivity,
    contactSources,
    inviteEligible,
  ] = await Promise.all([
    safe('campaign filters', Promise.all([queries.getCsmList(), queries.getAccountList(options.csmId)])),
    safe('campaign details by type', queries.getCampaignDetailsTable(options.csmId, options.accountId, startDate, endDate, options.groupByLocation)),
    safe('campaign details by name', queries.getCampaignNameDetails(options.csmId, options.accountId, startDate, endDate, options.groupByLocation)),
    options.groupByLocation
      ? safe('campaign type totals', queries.getCampaignDetailsTable(options.csmId, options.accountId, startDate, endDate, false))
      : Promise.resolve(undefined),
    options.groupByLocation
      ? safe('campaign name totals', queries.getCampaignNameDetails(options.csmId, options.accountId, startDate, endDate, false))
      : Promise.resolve(undefined),
    safe('engagement metrics', queries.getEngagementMetrics(options.csmId, options.accountId, startDate, endDate)),
    safe('promotion names', queries.getPromotionNameList(options.csmId, options.accountId, startDate, endDate)),
    safe('subscriber timeline', queries.getSubscriberTimeline(options.csmId, options.accountId, startDate, endDate)),
    safe('contact activity', queries.getContactActivity(options.csmId, options.accountId, startDate, endDate, options.groupByLocation)),
    safe('contact sources', queries.getContactSources(options.csmId, options.accountId, startDate, endDate)),
    safe('invite eligible', queries.getInviteEligible(options.csmId, options.accountId)),
  ])

  return {
    filters,
    dateRange: { startDate, endDate },
    campaignDetails: { typeData, nameData, typeTotals, nameTotals },
    engagementMetrics,
    promotionNames,
    subscriberTimeline,
    contactActivity,
    contactSources,
    inviteEligible,
  }
}

function isError(value: unknown): value is { error: string } {
  return Boolean(value && typeof value === 'object' && 'error' in value)
}

function compactList<T>(items: T[] | undefined, limit = 5) {
  return Array.isArray(items) ? items.slice(0, limit) : []
}

function summarizeProduct(product: any): string {
  const lines: string[] = ['# Product Dashboard']

  if (isError(product.journey)) {
    lines.push(`- Customer Journey Readout: ${product.journey.error}`)
  } else if (product.journey) {
    lines.push(`- Customer Journey Readout: ${product.journey.calls_analyzed} calls analyzed through ${product.journey.window_end}`)
    lines.push(`- Biggest opportunity: ${product.journey.summary?.biggestOpportunity?.title ?? 'n/a'}`)
    lines.push(`- Biggest bottleneck: ${product.journey.summary?.biggestBottleneck?.title ?? 'n/a'}`)
  }

  if (!isError(product.marketing)) {
    lines.push(`- Marketing ads: ${product.marketing.summary?.totalLeads ?? 0} leads, $${product.marketing.summary?.averageCpl ?? 0} avg CPL`)
  }

  if (!isError(product.overview)) {
    lines.push(`- TapCards: ${product.overview.tapcards.activeUnits} active, ${product.overview.tapcards.inactiveUnits.length} activated but inactive, ${product.overview.tapcards.notYetActivatedUnits} not yet activated`)
    lines.push(`- Boxes: ${product.overview.touchpoints.activeUnits} active, ${product.overview.touchpoints.inactiveUnits.length} activated but inactive, ${product.overview.touchpoints.notYetActivatedUnits} not yet activated`)
    lines.push(`- Texting stages: ${product.overview.texting.stages.map((stage: any) => `${stage.label} ${stage.count}`).join('; ')}`)
  }

  if (!isError(product.seoData) && product.seoData) {
    lines.push(`- SEO: ${product.seoData.summary?.managed ?? 0} managed, ${product.seoData.summary?.waitingOnSeoSetup ?? 0} waiting setup, ${product.seoData.summary?.gbpAccessNotMatched ?? 0} GBP access not matched`)
  }

  for (const [segment, data] of Object.entries(product.transcripts ?? {})) {
    if (isError(data)) {
      lines.push(`- ${segment}: ${(data as { error: string }).error}`)
      continue
    }
    const stats = (data as any).stats
    lines.push(`- ${segment}: ${stats?.total ?? 0} calls, won ${stats?.closedWon ?? 0}, scheduled ${stats?.demoScheduled ?? 0}, open ${stats?.open ?? 0}, lost ${stats?.closedLost ?? 0}, unknown ${stats?.unknown ?? 0}`)
  }

  return lines.join('\n')
}

function summarizeDatabase(database: any): string {
  const source = database?.sourceEnv ? ` via ${database.sourceEnv}` : ''
  const host = database?.host ? ` (${database.host})` : ''
  const warning = database?.warning ? `\n- Database warning: ${database.warning}` : ''
  return `# Connection\n- Database: ${database?.mode ?? 'unknown'}${source}${host}${warning}`
}

function summarizeCampaigns(campaigns: any): string {
  const lines: string[] = ['# Campaigns Dashboard']
  lines.push(`- Date range: ${campaigns.dateRange.startDate} to ${campaigns.dateRange.endDate}`)

  if (isError(campaigns.filters)) {
    lines.push(`- Filters: ${campaigns.filters.error}`)
  } else {
    const [csms, accounts] = campaigns.filters
    lines.push(`- Filters: ${csms.length} support teammates, ${accounts.length} accounts`)
  }

  if (isError(campaigns.campaignDetails.typeData)) {
    lines.push(`- Campaign types: ${campaigns.campaignDetails.typeData.error}`)
  } else {
    lines.push(`- Campaign types: ${campaigns.campaignDetails.typeData.length} rows`)
    for (const row of compactList(campaigns.campaignDetails.typeData, 5)) {
      lines.push(`  - ${row.campaign_type ?? row.location_name ?? 'Unknown'}: ${row.times_used ?? 0} used, ${row.texts_sent ?? 0} texts, ${row.redeemed ?? 0} redeemed`)
    }
  }

  if (isError(campaigns.engagementMetrics)) {
    lines.push(`- Engagement metrics: ${campaigns.engagementMetrics.error}`)
  } else {
    lines.push(`- Engagement metric rows: ${campaigns.engagementMetrics.length}`)
  }

  if (isError(campaigns.contactSources)) {
    lines.push(`- Contact sources: ${campaigns.contactSources.error}`)
  } else {
    lines.push(`- Contact source rows: ${campaigns.contactSources.length}`)
  }

  if (isError(campaigns.inviteEligible)) {
    lines.push(`- Invite eligible: ${campaigns.inviteEligible.error}`)
  } else {
    lines.push(`- Invite eligible: ${campaigns.inviteEligible.length}`)
  }

  return lines.join('\n')
}

async function main() {
  const options = parseArgs(process.argv.slice(2))
  process.chdir(DASHBOARD_DIR)
  loadEnvFile(path.join(DASHBOARD_DIR, '.env.local'))
  loadEnvFile(path.join(DASHBOARD_DIR, '.env'))

  const result: Record<string, unknown> = {
    generatedAt: new Date().toISOString(),
    options,
  }

  result.database = configureDatabaseForQueries(options)

  if (options.section === 'all' || options.section === 'product') {
    result.product = await loadProductStats(options)
  }
  if (options.section === 'all' || options.section === 'campaigns') {
    result.campaigns = await loadCampaignStats(options)
  }

  if (options.out) {
    fs.writeFileSync(options.out, JSON.stringify(result, null, 2))
  }

  if (options.format === 'json') {
    console.log(JSON.stringify(result, null, 2))
    return
  }

  const sections: string[] = []
  sections.push(summarizeDatabase(result.database))
  if (result.product) sections.push(summarizeProduct(result.product))
  if (result.campaigns) sections.push(summarizeCampaigns(result.campaigns))
  if (options.out) sections.push(`\nFull JSON written to ${options.out}`)
  console.log(sections.join('\n\n'))
}

main().catch(error => {
  console.error(error instanceof Error ? error.stack ?? error.message : error)
  process.exit(1)
})
