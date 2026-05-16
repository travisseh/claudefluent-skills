# Marketing Skill Registry

Detailed reference for each marketing skill. The main SKILL.md has a quick-reference table; this file has full capabilities, example prompts, and integration points.

---

## 1. Guide Writer (`/guide-writer`)

**Location:** `.claude/skills/guide-writer/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Creates evergreen how-to guides for ClaudeFluent
- Targets specific personas (Priya the PM, Derek the solo founder, Ashley the PMM, Sandra the VP CS)
- Extremely practical, zero-fluff content optimized for SEO longevity

**Example prompts:**
- "Write a guide on setting up MCP servers with Claude Code"
- "Create a deep dive guide on plan mode"
- "Write a beginner's guide to Claude Code for product managers"

**Integration points:**
- Output feeds into → `/behavior-design` (audit), `/gsc-submit` (index), `$travisse-writing-style` (distribute)
- Measures success via → `/funnel-optimization` (PostHog traffic + conversions)

---

## 2. Article Writer (`/article-writer`)

**Location:** `.claude/skills/article-writer/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Creates timely, opinionated thought leadership content
- More editorial voice than guides — takes stances, shares hot takes
- Designed to drive social sharing and discussion

**Example prompts:**
- "Write an article about why product managers should learn Claude Code"
- "Draft a hot take on the AI coding tool landscape"
- "Write about lessons learned from teaching 100+ students"

**Integration points:**
- Same as Guide Writer: → `/behavior-design` → `/gsc-submit` → `$travisse-writing-style`
- Articles tend to perform better on LinkedIn than guides

---

## 3. GSC Submit (`/gsc-submit`)

**Location:** `claude_course/website/.claude/skills/gsc-submit/SKILL.md`
**Scope:** Project (claude_course/website)

**What it does:**
- Submits new URLs to Google Search Console for indexing
- Should be run after every new guide or article is deployed
- Helps new content get discovered in search faster

**Example prompts:**
- "Submit the new guide to Google Search Console"
- "Index our latest guides in GSC"
- "Submit sitemap"

**Integration points:**
- Triggered after → content deployment (guide or article)
- Success measured via → `/funnel-optimization` (organic search traffic)

---

## 4. Funnel Optimization (`/funnel-optimization`)

**Location:** `.claude/skills/funnel-optimization/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Queries PostHog for conversion funnel data
- Identifies drop-off points in the signup flow
- Diagnoses conversion issues with data-driven recommendations
- Tracks custom events and A/B test results

**Example prompts:**
- "How is the site converting?"
- "Where are we losing people in the funnel?"
- "What does PostHog say about last week's traffic?"
- "Check analytics on the pricing page"

**Integration points:**
- Feeds data to → `/behavior-design` (audit weak pages), `/stripe` (correlate with revenue)
- Informed by → `/stripe` (revenue context)

---

## 5. Travisse Writing Style (`$travisse-writing-style`)

**Location:** `~/.codex/skills/travisse-writing-style/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Handles LinkedIn posts, articles, emails, and other writing in Travisse's voice
- Includes the LinkedIn-specific patterns and long-form rules
- Acts as the single source of truth for hooks, structure, tone, and formatting
- Primary organic distribution channel for ClaudeFluent

**Example prompts:**
- "Draft a LinkedIn post promoting the new MCP guide"
- "Write a LinkedIn thread about what I learned teaching Claude Code"
- "Create a hook-focused post about the pricing change"

**Integration points:**
- Distributes content from → `/guide-writer`, `/article-writer`
- Should be sharpened by → `/behavior-design` (hooks and CTAs)
- Performance tracked via → LinkedIn analytics (manual) + `/funnel-optimization` (UTM traffic)

---

## 6. Behavior Design (`/behavior-design`)

**Location:** `.claude/skills/behavior-design/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Audits any asset using Cialdini's persuasion principles
- Evaluates game mechanics and direct response advertising patterns
- Reviews landing pages, PRDs, marketing assets, product ideas
- Identifies gaps and provides specific, concrete recommendations

**Example prompts:**
- "Audit the ClaudeFluent landing page for persuasion gaps"
- "Review this email sequence for behavior design principles"
- "How can we make the pricing page more compelling?"

**Integration points:**
- Audits output from → every content/page skill
- Recommendations validated by → `$synthetic-user-feedback`
- Especially powerful when combined with `/funnel-optimization` data

---

## 7. Pricing, Packaging & Positioning (`/pricing-packaging-positioning`)

**Location:** `.claude/skills/pricing-packaging-positioning/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Strategic pricing advisor using Hormozi, Dunford, Campbell, Enns, Ramanujam, Ries & Trout frameworks
- Evaluates offers, tier structures, pricing strategy
- Positioning against competitors
- Packaging bundles and feature allocation

**Example prompts:**
- "Should we add a new pricing tier?"
- "Evaluate our current offer against Hormozi's value equation"
- "How should we position against competitor X?"
- "Review our pricing page copy and structure"

**Integration points:**
- Informed by → `/stripe` (revenue data, enrollment trends)
- Output audited by → `/behavior-design` (how pricing is presented)
- Validated by → `$synthetic-user-feedback` (simulated buyer reactions)

---

## 8. Synthetic User Feedback (`$synthetic-user-feedback`)

**Location:** `.claude/skills/synthetic-user-feedback/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Simulates real user feedback with persona-based testing
- Evaluates usability, purchase resonance, and message effectiveness
- Provides structured feedback from multiple simulated perspectives

**Example prompts:**
- "Test the new landing page with synthetic users"
- "How would a senior PM react to this pricing page?"
- "Simulate user feedback on this guide"

**Integration points:**
- Validates changes from → `/behavior-design`, `/pricing-packaging-positioning`
- Tests content from → `/guide-writer`, `/article-writer`
- Use before deploying significant changes

---

## 9. Stripe (`/stripe`)

**Location:** `.claude/skills/stripe/SKILL.md`
**Scope:** Project (personal repo)

**What it does:**
- Queries Stripe for ClaudeFluent enrollment and revenue data
- Pulls customer data, session info, waitlist numbers
- Tracks signups, churn, MRR, and payment failures

**Example prompts:**
- "How many signups this week?"
- "What's our current MRR?"
- "Pull enrollment data for the last 30 days"
- "Any failed payments or churn?"

**Integration points:**
- Provides context for → `/funnel-optimization` (revenue vs traffic), `/pricing-packaging-positioning` (pricing decisions)
- First step in → Conversion Audit workflow, Weekly Marketing Pulse
