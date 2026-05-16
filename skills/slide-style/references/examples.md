# Slide Content Examples

## Example 1: Feature Introduction Slide

**Good:**
```
H1: Claude Code Memory
H3: Persistent context that follows you across sessions
HR
H3: What Is It?
- Claude automatically saves notes to `~/.claude/projects/<project>/memory/MEMORY.md`
- First **200 lines** of MEMORY.md are loaded into every conversation
- Claude decides what to remember — patterns, preferences, architecture decisions
HR
H3: Try It
[code block with copy-pasteable commands]
```

**Why it works:** Starts with a clear title, gives context in the subtitle, uses bold labels in bullets, ends with something actionable.

## Example 2: Comparison Slide

**Good:**
```
H1: Plugins vs Skills
H3: Two ways to extend Claude Code
HR
H3: Skills
- Single SKILL.md file with instructions
- Claude triggers automatically based on context
- Good for: specific workflows, writing guides, project conventions
HR
H3: Plugins
- Bundle of skills + commands + agents + state
- User triggers via slash commands
- Good for: orchestrating multiple skills, persistent memory, complex workflows
HR
H3: When to Use Which
- **One-off workflow** → Skill
- **Ongoing system with state** → Plugin
```

**Why it works:** Parallel structure, equal treatment of both sides, practical decision guide at the end.

## Example 3: Exercise Slide

**Good:**
```
H1: Exercise: Build Your First Automation
H3: 1. Set up the project
[code block with setup prompt]
H3: 2. Add the core feature
[code block with feature prompt]
H3: 3. Deploy it
[code block with deploy prompt]
**Demo:** Everyone share their live URL.
```

**Why it works:** Numbered steps, each with a concrete prompt, ends with a social proof moment.

## Anti-Pattern Examples

**Bad:** Wall of text in a paragraph explaining a concept. Use bullets instead.

**Bad:** 8+ bullets in a single list. Split into two sections with an HR.

**Bad:** "Claude Code is a revolutionary tool that changes the way developers..." — Use specific, practical language instead.
