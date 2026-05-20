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

## Software Engineering Laws Lens

Use https://lawsofsoftwareengineering.com/ as a compact checklist of durable engineering principles when judging AI coding advice. The point is not to cite every law. The point is to notice when a workflow respects or violates laws that still matter when agents write the code.

### Architecture and Design

- Conway's Law: advice is stronger when it accounts for team boundaries, review ownership, and communication paths, not just individual prompting.
- Hyrum's Law: be suspicious of agents changing observable behavior casually; production users may depend on undocumented behavior.
- Gall's Law: prefer workflows that evolve working simple systems into richer systems instead of asking agents for a large replacement in one pass.
- Law of Leaky Abstractions: good agent workflows inspect the real code and runtime behavior underneath abstractions.
- Tesler's Law: complexity can move between code, prompts, product rules, tests, and operations; it rarely disappears.
- Second-System Effect: down-rank "rewrite it with AI" enthusiasm unless the source explains migration, compatibility, and rollback.
- Fallacies of Distributed Computing and CAP: distributed systems advice should discuss latency, failure, consistency, and partition tradeoffs explicitly.
- YAGNI, KISS, DRY, SOLID, Law of Demeter, and Principle of Least Astonishment: prefer content that uses AI to make code smaller, clearer, and more predictable, not merely more abstract.

### Planning and Estimation

- Brooks's Law, Ringelmann Effect, Price's Law, and Bus Factor: more agents or more humans are not automatically more throughput; look for ownership, handoff, and knowledge-spread mechanics.
- Parkinson's Law, Hofstadter's Law, and the Ninety-Ninety Rule: strong workflows keep scope small, maintain visible progress, and verify the last hard 10%.
- Goodhart's Law: be skeptical of proxy metrics such as lines changed, PR count, token volume, or benchmark wins when the goal is maintainable production code.
- Gilb's Law: prefer practitioners who define observable quality signals, even imperfect ones, over vague claims that "the AI made it better."
- Pareto Principle: look for advice that identifies the small number of review, context, test, and architecture moves that prevent most AI-code failures.

### Quality and Maintenance

- Boy Scout Rule and Broken Windows Theory: high-signal workflows leave code incrementally better and fix local messes that would otherwise train future agents into worse edits.
- Technical Debt: treat debt as anything that slows future change, including prompt-only knowledge, missing tests, unclear boundaries, and brittle generated code.
- Murphy's Law: prefer workflows that assume agent mistakes will happen and put checks, tests, review, and rollback in the path.
- Postel's Law: useful when discussing interfaces, but watch for advice that accepts sloppy inputs without protecting internal invariants.
- Kernighan's Law: generated cleverness is dangerous; if debugging will be harder than writing, make the agent simplify.
- Testing Pyramid and Pesticide Paradox: favor fast, layered tests and occasional new test angles instead of only replaying the same happy-path checks.
- Lehman's Laws: long-lived software must keep evolving; good AI workflows include maintenance, migration, and cleanup, not just first implementation.
- Linus's Law: review can help, but only when reviewers have enough context and the change is small enough to inspect.

### Decision-Making

- Dunning-Kruger, Confirmation Bias, and The Map Is Not the Territory: down-rank confident agent takes that do not inspect the repo, logs, product behavior, or user reality.
- Occam's Razor and Hanlon's Razor: prefer simple explanations and avoid inventing intent behind confusing code before checking history and constraints.
- Sunk Cost Fallacy: a bad generated implementation should be deleted quickly once evidence shows it is the wrong path.
- Hype Cycle and Amara's Law: current model hype should not replace durable workflow discipline; still watch for long-run capability changes that alter the workflow.
- Lindy Effect: stable engineering principles deserve more weight than fresh prompt tricks unless the new trick survives production use.
- First Principles Thinking and Inversion: strong sources break the problem down and ask how the project could fail before prescribing tools.

## Retrieval Workflow

When the user asks a question:

1. Identify the concrete question:
   - Is it about research/planning?
   - context engineering?
   - code review and quality?
   - agent autonomy?
   - tools such as Claude Code, Codex, OpenCode, Cursor, Ralph, AI SDK, MCP, or skills?
   - team workflow and production engineering?
   - which durable engineering law or failure mode is the question really about?

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
   - Which software engineering laws the advice respects or violates, when useful.
   - Any disagreement or uncertainty between sources.
   - A short "what I would try next" recommendation.

## Quality Bar

Bias toward sources that are:

- Production-minded over demo-minded.
- Skeptical of vibes and magic prompts.
- Specific about workflows, code ownership, testing, review, and failure modes.
- Aligned with durable software engineering laws: small slices, simple systems, explicit tradeoffs, real tests, and readable code.
- Useful for senior/product-minded engineers who care about durable code quality.

Avoid or down-rank sources that are:

- Mostly hype, tool affiliate content, or prompt-pack content.
- Focused on toy app generation without maintenance or production concerns.
- Unwilling to discuss failure modes.
- Pure model-release commentary unless it changes the workflow.
- Blind to classic failure modes: second-system rewrites, Goodharted metrics, leaky abstractions, clever code that is hard to debug, or unreviewable changes.

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
