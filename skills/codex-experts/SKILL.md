---
name: codex-experts
description: Search official OpenAI Codex docs plus a curated panel of Codex, AI coding agent, product-engineering, and agentic-workflow experts across X/Twitter and YouTube. Use when Travisse asks what the experts or official docs say about OpenAI Codex, Codex CLI, Codex desktop/app, Codex web/cloud, AGENTS.md, Codex skills, subagents, plugins, MCP, coding-agent workflows, or recent Codex practice. This skill routes YouTube work through youtube-transcript and X/Twitter work through x-api.
---

# Codex Experts

Use this skill to answer questions by searching official OpenAI Codex documentation and recent content from Travisse's curated Codex expert panel.

## Source skills

Reference and follow these skills for the actual retrieval mechanics:

- `/Users/you/Programming/personal-master/personal/.agents/skills/x-api/SKILL.md`
- `/Users/you/Programming/personal-master/personal/.agents/skills/youtube-transcript/SKILL.md`

Do not reimplement their credential, pricing, or transcript workflows here. This skill is the routing and research strategy layer.

## Expert roster

### Official documentation

- Codex docs home: `https://developers.openai.com/codex`
- Codex CLI: `https://developers.openai.com/codex/cli`
- Codex app: `https://developers.openai.com/codex/app`
- Codex IDE extension: `https://developers.openai.com/codex/ide`
- Codex web/cloud: `https://developers.openai.com/codex/cloud`
- Codex use cases: `https://developers.openai.com/codex/explore`
- Codex best practices: `https://developers.openai.com/codex/learn/best-practices`
- Codex videos: `https://developers.openai.com/codex/videos`
- Codex changelog: `https://developers.openai.com/codex/changelog`
- Codex feature maturity: `https://developers.openai.com/codex/feature-maturity`
- Open source Codex repo: `https://github.com/openai/codex`

### Product and workflow docs

- Prompting: `https://developers.openai.com/codex/prompting`
- Customization: `https://developers.openai.com/codex/customization`
- Memories: `https://developers.openai.com/codex/memories`
- Sandboxing: `https://developers.openai.com/codex/sandboxing`
- Subagents: `https://developers.openai.com/codex/subagents`
- Workflows: `https://developers.openai.com/codex/workflows`
- Models: `https://developers.openai.com/codex/models`
- Cyber safety: `https://developers.openai.com/codex/cyber-safety`

### Configuration and automation docs

- Config basics: `https://developers.openai.com/codex/config-basic`
- Advanced config: `https://developers.openai.com/codex/config-advanced`
- Config reference: `https://developers.openai.com/codex/config-reference`
- Permissions: `https://developers.openai.com/codex/permissions`
- Rules: `https://developers.openai.com/codex/rules`
- Hooks: `https://developers.openai.com/codex/hooks`
- AGENTS.md: `https://developers.openai.com/codex/guides/agents-md`
- MCP: `https://developers.openai.com/codex/mcp`
- Plugins: `https://developers.openai.com/codex/plugins`
- Skills: `https://developers.openai.com/codex/skills`
- Non-interactive mode: `https://developers.openai.com/codex/noninteractive`
- Codex SDK: `https://developers.openai.com/codex/sdk`
- App server: `https://developers.openai.com/codex/app-server`
- GitHub Action: `https://developers.openai.com/codex/github-action`

### Integrations and administration docs

- GitHub integration: `https://developers.openai.com/codex/integrations/github`
- Slack integration: `https://developers.openai.com/codex/integrations/slack`
- Linear integration: `https://developers.openai.com/codex/integrations/linear`
- Agent approvals and security: `https://developers.openai.com/codex/agent-approvals-security`
- Remote connections: `https://developers.openai.com/codex/remote-connections`
- Internet access for cloud tasks: `https://developers.openai.com/codex/cloud/internet-access`
- Enterprise admin setup: `https://developers.openai.com/codex/enterprise/admin-setup`
- Enterprise governance: `https://developers.openai.com/codex/enterprise/governance`
- Managed configuration: `https://developers.openai.com/codex/enterprise/managed-configuration`

### YouTube

Start with official OpenAI Codex videos, then expand to community tutorials only when needed.

- OpenAI YouTube: `https://www.youtube.com/@OpenAI`
- OpenAI Developers / official developer video surface: `https://developers.openai.com/codex/videos`
- Peter Yang: `https://www.youtube.com/@PeterYangYT`
- Grace Leung: `https://www.youtube.com/@graceleungyl`

Community YouTube is intentionally less fixed than the X roster. For Codex-specific questions, search YouTube each time for recent Codex CLI/app/cloud demos, then only add a creator to the answer if the title, description, or transcript directly supports the question.

### X/Twitter

- Thomas Sottiaux: `https://x.com/thsottiaux`
  - Bias/use case: Codex workflows, agentic coding practice, applied AI engineering.
- Jason Liu: `https://x.com/jxnlco`
  - Bias/use case: agentic systems, evals, structured outputs, AI engineering, practical LLM workflows.
- Andrew Ambrosino: `https://x.com/ajambrosino`
  - Bias/use case: Codex, agentic coding workflows, AI product/building practice.
- OpenAI Developers: `https://x.com/OpenAIDevs`
  - Bias/use case: official OpenAI developer news, Codex releases, examples, docs, product updates.
- OpenAI: `https://x.com/OpenAI`
  - Bias/use case: official product announcements and major release context.

## Default workflow

1. Translate Travisse's question into 2-5 search concepts.
   - Example: "Should I teach Codex subagents?" becomes `subagents`, `Codex`, `parallel agents`, `workflow`, `training`.
   - Prefer precise Codex terms over generic words like `AI` or `coding`.
2. Check official OpenAI Codex docs first when the question is about features, commands, settings, permissions, workflows, product behavior, availability, security, pricing, models, or "how does this work?"
3. Search X first when the question is about very recent takes, fast-moving tool changes, opinions, short tactical advice, or what specific practitioners are doing.
4. Search YouTube first when the question asks for deep explanation, tutorials, workflows, demos, classes, or examples.
5. For YouTube, inspect recent video titles and descriptions before pulling transcripts. Only fetch transcripts for videos whose title/description plausibly matches the question.
6. Synthesize across sources. Do not dump raw docs, transcripts, or tweets. Attribute claims to the official docs or creator and link the source.

## Official docs strategy

Use official OpenAI docs as the ground truth for capabilities and constraints, then use expert sources for interpretation, examples, and current practice.

Start with targeted web searches against the official documentation domains:

```text
site:developers.openai.com/codex subagents
site:developers.openai.com/codex AGENTS.md
site:developers.openai.com/codex permissions sandboxing
site:developers.openai.com/codex "Codex CLI"
site:developers.openai.com/codex "Codex app"
site:developers.openai.com/codex "skills"
site:developers.openai.com/codex "MCP"
site:github.com/openai/codex "AGENTS.md"
```

Decision rules:

- For supported Codex behavior, prefer `developers.openai.com/codex/*`.
- For CLI implementation details, release notes, config examples, or open-source behavior, use `github.com/openai/codex` after checking the docs.
- For rapidly changing product details, browse the docs/changelog rather than relying on memory.
- If official docs and expert commentary conflict, state the conflict and treat official docs as authoritative unless the expert is clearly describing unreleased/beta behavior.
- Cite official docs separately from expert commentary so Travisse can tell "what OpenAI says" from "what practitioners recommend."

## X/Twitter search strategy

Use the `x-api` CLI from its skill directory:

```bash
cd /Users/you/Programming/personal-master/personal/.agents/skills/x-api
python3 scripts/x.py --format md search '(from:thsottiaux OR from:jxnlco OR from:ajambrosino OR from:OpenAIDevs OR from:OpenAI) (Codex OR "Codex CLI" OR "AGENTS.md" OR subagents OR "coding agent") -filter:retweets' --max 25
```

For a specific expert:

```bash
cd /Users/you/Programming/personal-master/personal/.agents/skills/x-api
python3 scripts/x.py --format md search 'from:jxnlco (Codex OR agents OR evals OR "coding agent") -filter:retweets' --max 20
```

For recent timeline scanning:

```bash
cd /Users/you/Programming/personal-master/personal/.agents/skills/x-api
python3 scripts/x.py --format md user-tweets thsottiaux --max 20
```

Decision rules:

- Start cheap: `--max 10` to `--max 25` per query is usually enough.
- Use `from:` searches with keyword filters before broad user timeline pulls.
- Search the full X roster together when the concept is broad.
- Search one user at a time when the query has an obvious owner.
- Add `-filter:retweets` unless retweets are explicitly relevant.
- If results are thin, try one broader query before pulling full recent timelines.
- Respect the `x-api` cost guardrail: anything over $2/run requires confirmation.

## YouTube search strategy

YouTube channels and surfaces:

- OpenAI YouTube: `https://www.youtube.com/@OpenAI`
- Official OpenAI Codex videos: `https://developers.openai.com/codex/videos`
- Peter Yang: `https://www.youtube.com/@PeterYangYT`
- Grace Leung: `https://www.youtube.com/@graceleungyl`

Start by finding recent videos and matching by title/description. Use lightweight web or YouTube search queries such as:

```text
site:youtube.com/@OpenAI Codex
site:youtube.com "OpenAI Codex CLI" tutorial
site:youtube.com "Codex app" "OpenAI"
site:youtube.com "Codex subagents"
site:youtube.com "AGENTS.md" "Codex"
site:youtube.com/@PeterYangYT Codex
site:youtube.com/@graceleungyl Codex
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
- Prefer official OpenAI videos for product walkthroughs, then community videos for practical workflow examples.
- If titles are ambiguous, open the video page or description before transcript retrieval.
- When using transcripts, extract only the sections that answer the question and cite the video.

## Answer format

Lead with the answer, not the research log.

Recommended structure:

- `Short answer:` one direct judgment or summary.
- `Official baseline:` what OpenAI docs say, with links.
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
