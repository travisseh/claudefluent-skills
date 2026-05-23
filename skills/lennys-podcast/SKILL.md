---
name: lennys-podcast
description: Search and analyze Lenny Rachitsky podcast transcripts using the lennysdata MCP server. Use for product strategy, product management practices, growth tactics, company-building insights, or topics Lenny has covered with product leaders.
---

# Lenny's Podcast Research

Search and analyze Lenny Rachitsky's podcast transcripts using the lennysdata MCP server. Use when researching product strategy, product management practices, growth tactics, company-building insights, or any topic Lenny has covered with top product leaders.

## MCP Setup

The `lennysdata` MCP server provides access to the full Lenny's Podcast transcript archive. It was added via:

```bash
claude mcp add lennysdata --transport http https://mcp.lennysdata.com/mcp --header "Authorization: Bearer <token>"
```

Token is stored in local `.claude.json`. Expires periodically — if you get auth errors, ask the user to refresh the token at lennysdata.com.

## When to Use

- Researching how specific companies build product (Linear, Stripe, Notion, Airbnb, etc.)
- Looking for frameworks and methodologies (PMF engine, Shape Up, empowered teams, etc.)
- Finding quotes and insights from specific founders/leaders
- Analyzing trends in product management, growth, engineering culture
- Preparing for meetings or proposals that need data-backed product strategy arguments

## How to Use

1. Use `ToolSearch` to find available `mcp__lennysdata__*` tools
2. Search for episodes by topic, guest name, or keyword
3. Pull full transcripts for deep analysis
4. Extract specific quotes, frameworks, and actionable insights

## Tips

- Search broadly first (e.g., "product engineers") then drill into specific episodes
- Many episodes have both a guest interview AND Lenny's commentary — both are valuable
- Cross-reference findings with the product-brain plugin state files for Example Company-specific context
- When extracting insights for proposals, always note the episode and guest for attribution
