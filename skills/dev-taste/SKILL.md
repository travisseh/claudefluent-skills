---
name: dev-taste
description: Find and synthesize high-signal YouTube sources about AI-assisted software development, coding agents, context engineering, and workflows for getting production-quality code from AI. Use when the user asks what serious AI coding practitioners are saying, wants recent videos/talks, asks how to get higher-quality production code from AI, or wants taste-filtered recommendations from YouTube.
---

# Dev Taste

Use this skill as a taste filter for practical, production-minded AI coding content. The goal is not general AI news. The goal is to find people and talks that help Travisse get actual high-quality production code from AI coding agents.

## Default Sources

Start with these sources before doing a wider search.

### Dexter Horthy / HumanLayer

- Person: Dexter Horthy, founder of HumanLayer.
- Focus: coding agents in real production codebases, context engineering, Research-Plan-Implement, CRISPI/QRSPI, human-in-the-loop review, code quality, avoiding AI slop.
- Primary site: https://humanlayer.dev
- Useful search queries:
  - `Dexter Horthy HumanLayer coding agents`
  - `Dex Horthy HumanLayer context engineering`
  - `Dexter Horthy Research Plan Implement`
  - `Dexter Horthy No Vibes Allowed`
  - `Dexter Horthy CRISPI`
- Known relevant videos:
  - AI Engineer talk channel: https://www.youtube.com/@aiDotEngineer
  - AIE Miami livestream containing "Everything We Got Wrong About RPI": https://www.youtube.com/watch?v=6IxSbMhT7v4
  - MLOps.community version/search result: https://www.youtube.com/@MLOps
  - "No Vibes Allowed" search target on AI Engineer: https://www.youtube.com/@aiDotEngineer
- Known useful concepts:
  - Read the code; do not deeply review thousand-line plans instead of code.
  - Research should be objective and factual, not polluted by premature implementation opinions.
  - Convert tickets into questions before research.
  - Split giant prompts into smaller workflow phases because models have an instruction budget.
  - Prefer vertical implementation slices with checks over horizontal layer-by-layer plans.
  - 2-3x speedups with code ownership beat lights-out slop factories.

### AI Engineer

- Channel: https://www.youtube.com/@aiDotEngineer
- Focus: conference talks from serious AI engineering practitioners.
- Use for: talks from Dexter Horthy, swyx, OpenAI, Cursor, Anthropic, Cognition, Vercel, and other builders discussing agent workflows, evals, context engineering, product engineering, and production AI systems.
- Search strategy:
  - Search within YouTube for `site:youtube.com/@aiDotEngineer <topic>` when web search is available.
  - With `yt-dlp`, use `ytsearch10:<topic> AI Engineer coding agents production code`.
  - Prefer recent talks, but do not ignore older high-signal talks if they became canonical.

### Matt Pocock / AI Hero

- Person: Matt Pocock.
- Why included: creator/source of the `grill-me` skill pattern used for relentless requirement and design interrogation.
- Evidence/source article: https://www.aihero.dev/my-grill-me-skill-has-gone-viral
- Channel: https://www.youtube.com/@mattpocockuk
- AI Hero: https://www.aihero.dev
- Focus: practical AI engineering for web developers, Claude Code workflows, skill-based workflows, planning, PRDs, tracer bullets, AI SDK, TypeScript.
- Useful search queries:
  - `Matt Pocock Claude Code AI coding agents`
  - `Matt Pocock grill me skill`
  - `Matt Pocock AI Hero coding agents`
  - `Matt Pocock production AI engineering`
- Known relevant video:
  - `Building a REAL feature with Claude Code: every step explained` on Matt Pocock's channel.

## Retrieval Workflow

When the user asks a question:

1. Identify the concrete question:
   - Is it about research/planning?
   - context engineering?
   - code review and quality?
   - agent autonomy?
   - tools such as Claude Code, Codex, OpenCode, Cursor, Ralph, AI SDK, MCP, or skills?
   - team workflow and production engineering?

2. Search YouTube from the default sources first:

```bash
yt-dlp --flat-playlist --print '%(upload_date)s|%(channel)s|%(channel_url)s|%(webpage_url)s|%(title)s' \
  'ytsearch10:<query terms>'
```

3. Prefer videos that match at least two of these:
   - The speaker has shipped or advised production teams, not just made demos.
   - The content discusses failure modes, review, evals, testing, architecture, or brownfield codebases.
   - The content gives a workflow that can be tried in Travisse's own coding practice.
   - The video is recent enough to reflect current agent capabilities.
   - The video has a transcript available.

4. Use `$youtube-transcript` to pull the transcript for the best candidate videos before summarizing. Do not summarize based only on title or thumbnail.

5. Answer with:
   - Best videos to watch, with clickable URLs.
   - Why each video is relevant to the user's question.
   - The strongest actionable takeaways.
   - Any disagreement or uncertainty between sources.
   - A short "what I would try next" recommendation.

## Quality Bar

Bias toward sources that are:

- Production-minded over demo-minded.
- Skeptical of vibes and magic prompts.
- Specific about workflows, code ownership, testing, review, and failure modes.
- Useful for senior/product-minded engineers who care about durable code quality.

Avoid or down-rank sources that are:

- Mostly hype, tool affiliate content, or prompt-pack content.
- Focused on toy app generation without maintenance or production concerns.
- Unwilling to discuss failure modes.
- Pure model-release commentary unless it changes the workflow.

## Useful Search Templates

```bash
yt-dlp --flat-playlist --print '%(upload_date)s|%(channel)s|%(channel_url)s|%(webpage_url)s|%(title)s' \
  'ytsearch10:Dexter Horthy HumanLayer coding agents production code'

yt-dlp --flat-playlist --print '%(upload_date)s|%(channel)s|%(channel_url)s|%(webpage_url)s|%(title)s' \
  'ytsearch10:AI Engineer context engineering coding agents production'

yt-dlp --flat-playlist --print '%(upload_date)s|%(channel)s|%(channel_url)s|%(webpage_url)s|%(title)s' \
  'ytsearch10:Matt Pocock Claude Code production feature AI Hero'
```

## Standing Opinion

The current best bet for high-quality AI-coded production software is not "more autonomy everywhere." It is a disciplined workflow:

- clarify requirements with aggressive questioning,
- research the codebase factually,
- make architecture and design choices explicit,
- slice work vertically,
- let agents implement,
- read the code,
- verify behavior with tests and product-level checks.

Treat new videos as evidence that may update this opinion, not as automatic truth.
