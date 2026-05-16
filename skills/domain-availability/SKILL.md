---
name: domain-availability
description: "Check domain name availability using Namecheap via Playwright. Use this skill whenever the user is brainstorming names for a project, product, course, or business and wants to check if domains are available. Also trigger when they ask 'is X.com available', 'check domains for', 'find me a domain', or are naming anything and might need to verify domain availability. Triggers on: domain availability, check domain, is this domain taken, find a domain, domain name, .com available, naming a project, brainstorm names."
---

# Domain Availability Checker

Check if domain names are available for registration using Namecheap.

## When to Use

- User needs to find an available domain name
- User wants to check multiple domain name ideas
- User is brainstorming names for a project/product/course

## How It Works

Use Playwright to check domain availability on Namecheap:

1. Navigate to: `https://www.namecheap.com/domains/registration/results/?domain={domain_name_without_tld}`
2. Wait 2 seconds for results to load
3. Check the page snapshot for availability status

## Reading Results

**Available domains show:**
- Price (e.g., "$11.28/yr")
- "Add to cart" button
- Promo codes like "$6.49 WITH NEWCOM649"

**Taken domains show:**
- "Taken" label
- "Make offer" button instead of "Add to cart"

**Premium domains show:**
- "Premium" label
- High price (e.g., "$2,999.00")

## Example Workflow

```
1. User: "Help me find a domain for my AI course"

2. Brainstorm name ideas first (don't check yet)

3. Check each promising .com domain:
   - Navigate to Namecheap URL with domain name
   - Wait 2 seconds
   - Read snapshot for status

4. Compile results:
   - Available .com domains with prices
   - Taken domains
   - Alternative TLDs if .com is taken (.ai, .dev, .io, .app)

5. Make recommendations based on:
   - Availability
   - Price
   - Memorability
   - Relevance to the project
```

## Common TLD Pricing (approximate)

- .com - $11-15/yr
- .ai - $80/yr (2-year minimum)
- .io - $35/yr
- .dev - $13/yr (requires HTTPS)
- .app - $13/yr (requires HTTPS)
- .co - $30/yr

## Tips

- Check .com first - it's the most trusted
- If .com is taken, .ai is good for AI-related projects
- .dev and .io work well for technical audiences
- Avoid obscure TLDs (.xyz, .club) for professional use
- Watch for "Premium" domains - they're technically available but expensive
- Per David Placek (Lexicon Branding): "The .com has become an area code." Domain shouldn't drive the name choice. Get the right name first, solve the domain later.

## Naming Framework (David Placek / Lexicon Branding)

When brainstorming names (not just checking availability), apply this framework from the man who named Pentium, BlackBerry, Swiffer, Sonos, Vercel, and Windsurf.

### The 3 Requirements of the Right Name

Every good name satisfies ALL THREE simultaneously:
1. **Original** — distinct from everything in the category
2. **Processing Fluent** — easy for the brain. Familiar parts assembled unexpectedly. "Surprisingly familiar."
3. **Surprising** — creates a double-take. If the team is comfortable with it, it's probably wrong.

### Sound Symbolism (Power Letters)

Every letter sends a psychological signal. Prioritize these in name candidates:
- **V** — most alive/vibrant sound (Corvette, Viagra, Vercel)
- **B** — most reliable sound (BlackBerry)
- **X** — innovation, speed, crispness (SpaceX, Lexus)
- **K** — strong, explosive
- **Z** — noisy, attention-commanding (Azure)
- **S** — signal-creating (Sonos)
- **P** — fast, reliable
- **D** — fast

### Structural Patterns

- **CVCV (consonant-vowel-consonant-vowel)** — how children learn language (mama, dada). Most naturally fluent structure. (Sonos, Turo, Kova)
- **Compound words (1+1=3)** — two words each bring their own web of associations, creating richer meaning than either alone. (WindSurf, PowerBook, BlackBerry, DreamWorks)

### Generation Rules

1. **Quantity leads to quality.** 200 names is not enough. Get to 1,500. Most are trash. That's the point.
2. **Separate creation from evaluation.** Never judge while generating.
3. **Never describe, always suggest.** Descriptive names (ProMop, CloudPro, InfoSeek) are comfortable and invisible. Suggestive names (Swiffer, Google, Impossible) create experiences.
4. **The Polarization Principle.** Half the team hating it + half loving it = strong signal. Unanimous approval = invisible zone.
5. **Synchronicity.** Pull inspiration from unrelated domains. If naming a tech company, read hunting magazines. 30% of the time you'll find something.
6. **Invented names cost LESS to build into brands** than existing words, despite the common myth.

### Evaluation Tests

- **The Competitor Test.** Don't ask "what do you think of this name?" Instead: "We have a new competitor called [X]. How do you feel?" This reveals marketplace behavior.
- **The Baseball Cap Test.** Would it look good stitched on a hat?
- **The WSJ Ad Test.** Mock it up in a headline. Does it carry weight?
- **The Identity Test.** Can a customer say "I'm [X] trained" or "I went through [X]"?
- **The Golden Response.** The best consumer reaction: "I don't know much about them, but they're not like the other guys."

### What Makes Names Weak

- Descriptive (ProMop lost to Swiffer — $200M vs $5B)
- Comfortable / consensus favorite
- Category-obvious language everyone else uses
- No power letters
- Tool-specific or platform-locked
