---
name: garments
description: "Order men's garments from store.churchofjesuschrist.org using dev-browser browser automation. Use when the user asks to order garments, restock garments, or buy temple clothing."
---

# Garment Ordering

Order men's garments from the Church of Jesus Christ online store using `$dev-browser`.

## Store URL

```
https://store.churchofjesuschrist.org/top-cat/clothing/men-s-clothing/men-s-garments/5637160344.c
```

## the user's Garment Specs

### Tops
- **Style:** Stretch Cotton Lower Crew
- **Size:** Large
- **Length:** Short

### Bottoms
- **Style:** Dry Stretch Support Brief
- **Size:** Large
- **Length:** Short

## Browser Path

Use `dev-browser --connect` and a named page such as `browser.getPage("lds-store")`.

## Workflow

1. Connect to the live browser and open the garments category URL
2. Use Playwright locators to work through the product selectors
3. Navigate to tops section, select "Stretch Cotton Lower Crew"
4. Select size Large, length Short
5. Set quantity as requested
6. Add to cart
7. Repeat for bottoms: select "Dry Stretch Support Brief", Large, Short
8. Set quantity as requested
9. Add to cart
10. Navigate to cart, review totals

## Safety Rules

1. **NEVER complete a purchase without showing the total and getting explicit approval**
2. **NEVER enter payment info** — only use saved payment methods
3. **Show cart contents and total before checkout**
4. If login is required, tell the user — don't try to enter credentials

## Tips

- The store may require an LDS account login — if redirected to sign in, pause and tell the user
- Products may have multiple size/length/style selectors — screenshot each step to confirm correct options
- Prefer Playwright locators over coordinate clicking
- Always screenshot before and after adding to cart to confirm items
