---
name: cc-taste
description: Search official Anthropic Claude Code/Cowork docs plus a curated taste panel of Claude Code, Codex, AI coding agent, and product-engineering experts across YouTube and X/Twitter. Use when Travisse asks what the experts or official docs say about Claude Code, Codex, Cursor, Cowork, AI coding workflows, agentic development, product engineering with AI, wants recent expert content synthesized, or refers to cc taste / CC experts. This skill routes YouTube work through youtube-transcript and X/Twitter work through x-api.
---

# CC Taste

Use this skill to answer questions by searching official Anthropic Claude Code/Cowork documentation and recent content from Travisse's curated Claude Code / Codex expert panel.

## Source skills

Reference and follow these skills for the actual retrieval mechanics:

- `/Users/you/Programming/personal-master/personal/.agents/skills/x-api/SKILL.md`
- `/Users/you/Programming/personal-master/personal/.agents/skills/youtube-transcript/SKILL.md`

Do not reimplement their credential, pricing, or transcript workflows here. This skill is the routing and research strategy layer.

## Expert roster

### Official documentation

- Claude Code docs: `https://docs.anthropic.com/en/docs/claude-code/overview`
- Claude Code quickstart: `https://docs.anthropic.com/en/docs/claude-code/quickstart`
- Claude Code common workflows: `https://docs.anthropic.com/en/docs/claude-code/tutorials`
- Claude Code settings: `https://docs.anthropic.com/en/docs/claude-code/settings`
- Claude Code output styles: `https://docs.anthropic.com/en/docs/claude-code/output-styles`
- Claude Cowork docs: `https://claude.com/docs/cowork`
- Claude Cowork third-party provider docs: `https://claude.com/docs/cowork/3p/overview`

### YouTube

- Grace Leung: `https://www.youtube.com/@graceleungyl`
- Peter Yang: `https://www.youtube.com/@PeterYangYT`

### X/Twitter

- Felix Rieseberg: `https://x.com/felixrieseberg`
  - Bias/use case: Cowork, Electron, AI coding tools, developer tooling.
- Andrew Morris: `https://x.com/amorriscode`
  - Bias/use case: Claude Code.
- Bryan Cherny: `https://x.com/bcherny`
  - Bias/use case: Claude Code, Anthropic, developer tooling.

## Default workflow

1. Translate Travisse's question into 2-5 search concepts.
   - Example: "Should I teach subagents?" becomes `subagents`, `"Claude Code" agents`, `workflow`, `course`, `training`.
   - Prefer precise tool/product terms over generic words like `AI` or `coding`.
2. Check official Claude Code/Cowork docs first when the question is about features, commands, settings, permissions, workflows, product behavior, availability, security, or "how does this work?"
3. Search X first when the question is about very recent takes, fast-moving tool changes, opinions, or short tactical advice.
4. Search YouTube first when the question asks for deep explanation, tutorials, workflows, demos, classes, or examples.
5. For YouTube, inspect recent video titles and descriptions before pulling transcripts. Only fetch transcripts for videos whose title/description plausibly matches the question.
6. Synthesize across sources. Do not dump raw docs, transcripts, or tweets. Attribute claims to the official docs or creator and link the source.

## Official docs strategy

Use official docs as the ground truth for capabilities and constraints, then use expert sources for interpretation, examples, and current practice.

Start with targeted web searches against the official documentation domains:

```text
site:docs.anthropic.com/en/docs/claude-code subagents
site:docs.anthropic.com/en/docs/claude-code permissions settings
site:docs.anthropic.com/en/docs/claude-code "output styles"
site:claude.com/docs/cowork connectors
site:claude.com/docs/cowork "Claude Code"
```

Decision rules:

- For Claude Code behavior, prefer `docs.anthropic.com/en/docs/claude-code/*`.
- For Cowork behavior, prefer `claude.com/docs/cowork*`.
- For rapidly changing product details, browse the docs rather than relying on memory.
- If official docs and expert commentary conflict, state the conflict and treat official docs as authoritative unless the expert is clearly describing unreleased/beta behavior.
- Cite official docs separately from expert commentary so Travisse can tell "what Anthropic says" from "what practitioners recommend."

## X/Twitter search strategy

Use the `x-api` CLI from its skill directory:

```bash
cd /Users/you/Programming/personal-master/personal/.agents/skills/x-api
python3 scripts/x.py --format md search '(from:felixrieseberg OR from:amorriscode OR from:bcherny) ("Claude Code" OR Codex OR Cowork) -filter:retweets' --max 25
```

For a specific expert:

```bash
cd /Users/you/Programming/personal-master/personal/.agents/skills/x-api
python3 scripts/x.py --format md search 'from:amorriscode "Claude Code" -filter:retweets' --max 20
```

For recent timeline scanning:

```bash
cd /Users/you/Programming/personal-master/personal/.agents/skills/x-api
python3 scripts/x.py --format md user-tweets amorriscode --max 20
```

Decision rules:

- Start cheap: `--max 10` to `--max 25` per query is usually enough.
- Use `from:` searches with keyword filters before broad user timeline pulls.
- Search all three X experts together when the concept is broad.
- Search one user at a time when the query has an obvious owner, such as Cowork for Felix or Claude Code for Andrew/Bryan.
- Add `-filter:retweets` unless retweets are explicitly relevant.
- If results are thin, try one broader query before pulling full recent timelines.
- Respect the `x-api` cost guardrail: anything over $2/run requires confirmation.

## YouTube search strategy

YouTube channels:

- Grace Leung: `https://www.youtube.com/@graceleungyl`
- Peter Yang: `https://www.youtube.com/@PeterYangYT`

Start by finding recent videos and matching by title/description. Use lightweight web or YouTube search queries such as:

```text
site:youtube.com/@graceleungyl Claude Code
site:youtube.com/@PeterYangYT Codex
site:youtube.com/@graceleungyl "AI coding"
site:youtube.com/@PeterYangYT "Claude Code"
```

Only after a title/description match, fetch transcripts through the `youtube-transcript` skill:

```bash
uv run --with youtube-transcript-api python \
  /Users/you/.codex/skills/youtube-transcript/scripts/fetch_youtube_transcript.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format json
```

Decision rules:

- Pull at most 2-4 transcripts by default. Ask before pulling many more.
- Prefer newest relevant videos unless Travisse asks for "best" or evergreen advice.
- If titles are ambiguous, open the video page or description before transcript retrieval.
- When using transcripts, extract only the sections that answer the question and cite the video.

## Answer format

Lead with the answer, not the research log.

Recommended structure:

- `Short answer:` one direct judgment or summary.
- `Official baseline:` what Anthropic docs say, with links.
- `What the experts seem to be saying:` 3-6 bullets, each attributed.
- `Practical takeaways for Travisse:` 2-5 bullets grounded in his ClaudeFluent / product context when relevant.
- `Sources checked:` concise list of X searches, tweets, videos, or transcripts used.

## Guardrails

- Treat X as high-recency, lower-depth signal.
- Treat YouTube as lower-recency, higher-depth signal.
- Treat official docs as highest authority on supported behavior.
- Do not claim an expert believes something unless the content directly supports it.
- Separate direct evidence from inference.
- If evidence is sparse, say so and give the best next search rather than overfitting.
