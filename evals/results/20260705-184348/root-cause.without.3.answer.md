The issue is that `formatPrice` doesn't handle `null` values. When `cents` is `null`, dividing it results in `NaN`. Here's the fix:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This treats products with no price (`null`) as `$0.00`. If you'd prefer different behavior (like skipping them from the total entirely), you'd need to filter at the `cartTotalCents()` level instead, but the above fix addresses the NaN on the checkout page and handles all call sites uniformly.
