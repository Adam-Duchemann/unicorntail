The bug occurs when `priceCents` is `null`—it propagates through arithmetic as `NaN`. Fix `formatPrice()` to handle null, and ensure `cartTotalCents()` treats missing prices as 0:

```js
// pricing.js — shared
export function formatPrice(cents) {
  const amount = cents ?? 0;
  return `$${(amount / 100).toFixed(2)}`;
}
```

```js
// Wherever cartTotalCents is defined (likely cart.js or a utility)
function cartTotalCents(items) {
  return items.reduce((sum, item) => sum + (item.priceCents ?? 0), 0);
}
```

The `?? 0` operator treats null/undefined as 0, so products without prices render as $0.00 instead of $NaN, and the cart total calculates correctly even when some items lack a price.
