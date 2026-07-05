Looking at the code, the issue is that `formatPrice()` doesn't handle `null` or `NaN` values. When a product has no price, `priceCents` is `null`, and if `cartTotalCents()` processes items with null values, it may return `NaN`. The division by 100 then results in `NaN`, which gets stringified as `"$NaN"`.

Fix the `formatPrice` function to handle these cases:

```js
// pricing.js — shared
export function formatPrice(cents) {
  cents = Number.isFinite(cents) ? cents : 0;
  return `$${(cents / 100).toFixed(2)}`;
}
```

This safely converts `null`, `undefined`, and `NaN` values to `0`, so products without a price show as `$0.00` instead of `$NaN`. The `Number.isFinite()` check ensures any non-numeric or non-finite value defaults to zero.
