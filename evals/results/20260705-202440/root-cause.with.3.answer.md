```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This handles the `null` case in the shared function that all callers route through. When a product has no price yet, it displays as `$0.00` instead of `NaN`.

If you want to exclude unprice items from the cart total entirely instead, filter them in checkout.js:

```js
summary.total = formatPrice(cartTotalCents(items.filter(i => i.priceCents != null)));
```

The first fix (in `formatPrice`) is simpler and handles the immediate bug. Use the second only if items without prices should be excluded from the total.
