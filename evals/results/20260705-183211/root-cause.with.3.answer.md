The bug happens because `formatPrice()` and `cartTotalCents()` don't handle `null` prices. When a product has no price yet, `priceCents` is `null`, and arithmetic with `null` produces `NaN`.

Here's the fix:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) cents = 0;
  return `$${(cents / 100).toFixed(2)}`;
}
```

And update `cartTotalCents()` to treat missing prices as zero:

```js
// In whatever file defines cartTotalCents()
function cartTotalCents(items) {
  return items.reduce((sum, item) => sum + (item.priceCents ?? 0), 0);
}
```

This treats unprice items as $0.00 instead of NaN. If you want stricter behavior (prevent checkout entirely when prices are missing), that would go in the checkout page's validation logic, not here.
