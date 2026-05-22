---
name: errands
description: "Run virtual errands using dev-browser browser automation — shop Amazon, check shipping/tracking, place Instacart/Walmart/DoorDash orders, and handle other browser-based tasks. Use when the user asks to buy something, track a package, order groceries, find a product, compare prices, or do anything that requires browsing the web on his behalf."
---

# Virtual Errands

Use `$dev-browser` to handle real-world errands: shopping, tracking packages, placing orders, comparing products, and other browser-based tasks.

Use `dev-browser --connect` for live/authenticated sites and reuse named pages per site when practical.

## Safety Rules

1. **NEVER complete a purchase without explicit approval.** Always pause at the final checkout screen, show the total, and ask "Should I place this order?"
2. **NEVER enter payment info.** Rely on saved payment methods in the browser. If no saved payment, tell the user.
3. **NEVER change account settings, passwords, or subscriptions** unless explicitly asked.
4. **Show prices and totals** before any purchase decision.
5. **If a CAPTCHA or 2FA appears**, tell the user — don't try to solve it.

## Workflows

### Amazon Shopping

1. Connect with `dev-browser --connect` and reuse a named page like `browser.getPage("amazon")`
2. Open `https://www.amazon.com` or the direct product URL
3. Use Playwright locators to search, inspect results, and open product pages
7. For each product, extract: title, price, rating, review count, Prime eligibility, delivery date
8. Present comparison to the user
9. If approved, add to cart with locators and clicks
10. Navigate to `https://www.amazon.com/gp/cart/view.html`
11. **STOP and show cart total. Ask for approval before proceeding.**
12. If approved, proceed through checkout using saved payment/address

**Finding links in other apps (e.g., LinkedIn messages):**
- First open the source (LinkedIn messaging, email, etc.)
- Find and extract the Amazon URLs from the conversation
- Open each in a new tab to compare

### Package Tracking

1. Connect to the live browser
2. If given a tracking number/link directly, open it with `page.goto(...)`
3. If tracking carrier is known:
   - UPS: `https://www.ups.com/track?tracknum=TRACKING_NUMBER`
   - USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels=TRACKING_NUMBER`
   - FedEx: `https://www.fedex.com/fedextrack/?trknbr=TRACKING_NUMBER`
   - Amazon: `https://www.amazon.com/gp/your-account/order-history`
4. Read the page with locators, `textContent`, or `snapshotForAI`
5. Extract: current status, location, estimated delivery date, any exceptions
6. Report back concisely

### Instacart Orders

1. Open Instacart in the live browser
2. Select store if needed using locators and clicks
3. For each item:
   - Search with locators and fills
   - Pick best match and add to cart
   - Adjust quantity if needed
4. Review cart at `https://www.instacart.com/cart`
5. **STOP and show cart contents + total. Ask for approval.**
6. If approved, proceed to checkout with saved payment

### Walmart Orders (Grocery Pickup/Delivery)

1. Open Walmart in the live browser
2. Search and add items similar to Instacart flow
3. Review cart at `https://www.walmart.com/cart`
4. **STOP and show cart contents + total. Ask for approval.**
5. If approved, select pickup/delivery time slot, proceed with saved payment

### DoorDash Orders

1. Open DoorDash in the live browser
2. Search for restaurant or browse with locators and fills
3. Browse menu with locators, `textContent`, or `snapshotForAI`
4. Add items to cart and customize as needed
5. Review cart and show total
6. **STOP and show order summary + total + estimated delivery time. Ask for approval.**
7. If approved, proceed with saved payment

### Generic Web Errand

For anything else (booking appointments, filling out forms, researching, etc.):
1. Connect to the live browser
2. Navigate to the relevant site
3. Complete the task step by step
4. **Pause before any action that spends money, sends a message, or makes a commitment**
5. Report results

## Comparison Format

When comparing products or options, present as:

```
## [Category] Comparison

1. **[Product A]** — $XX.XX
   - [Key spec/feature]
   - [Rating]: X.X stars (X,XXX reviews)
   - [Delivery]: [date]
   - [Pros/Cons if relevant]

2. **[Product B]** — $XX.XX
   - ...

**Recommendation:** [Which one and why, based on price/reviews/Prime/delivery]
```

## Tips

- Prefer `browser.listPages()` if you need to inspect existing tabs
- Use Playwright locators instead of brittle coordinates when possible
- If a page is slow to load, wait explicitly or retry after a moment
- For long shopping lists, add items one at a time and confirm the cart periodically
- If logged out of a service, tell the user rather than trying to log in
