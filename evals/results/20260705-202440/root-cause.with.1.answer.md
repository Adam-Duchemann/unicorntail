The issue is that `formatPrice` doesn't handle `null` values. When `priceCents` is `null`, the division produces `0`, but if the total calculation somehow involves null in a way that propagates as `NaN`, or if other code paths call it with `NaN`/`undefined`, we get `"$NaN"`.

Fix `formatPrice` to handle null and NaN:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null || isNaN(cents)) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This treats products without a price (null) as $0.00 in the UI, preventing NaN from appearing in the total.
