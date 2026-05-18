# Search the Library

## Context
Find entries in the catalog by keyword when the user doesn't remember the exact name.

## Input
The user provides a keyword or description.

## Steps

### 1. Read the Catalog
- Read `library.yaml` (colocated with this skill)
- Parse all entries from `library.skills`, `library.agents`, `library.prompts`, `library.hooks`, `library.plugins`, and `library.mcp_servers`

### 2. Search
- Match the keyword (case-insensitive) against:
  - Entry `name`
  - Entry `description`
- A match is any entry where the keyword appears as a substring in either field
- Collect all matches across all types
- Also match against collection names in the `collections` section. If a collection name matches, include it in results with type `collection` and show the item count
- Also match against team names in the `teams` section. If a team name matches, include it in results with type `team` and show the collections count

### 3. Display Results

If matches found, format as:

```
## Search Results for "<keyword>"

| Type | Name | Description | Source |
|------|------|-------------|--------|
| skill | matching-skill | description... | source... |
| plugin | matching-plugin | description... | source... |
| mcp_server | matching-mcp | description... | — |
| collection | matching-collection | 4 items | — |
| team | matching-team | 3 collections | — |
```

If no matches:
```
No results found for "<keyword>".

Tip: Try broader keywords or run `/aos-library list` to see the full catalog.
```

### 4. Suggest Next Step
If matches were found, suggest: `Run /aos-library use <name> to install one of these.`
