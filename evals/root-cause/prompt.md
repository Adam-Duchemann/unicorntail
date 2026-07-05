Bug report: "The checkout page shows NaN for the total when a product has no price yet."

Relevant code:

```js
// pricing.js — shared
export function formatPrice(cents) {
  return `$${(cents / 100).toFixed(2)}`;
}

// cart.js
items.forEach(i => row.append(formatPrice(i.priceCents)));

// checkout.js  ← the page from the bug report
summary.total = formatPrice(cartTotalCents(items));

// email-receipt.js
lines.push(`${item.name}: ${formatPrice(item.priceCents)}`);
```

`priceCents` is `null` for products whose price isn't set yet. Fix the bug. Reply with the code directly. Do not create files.
