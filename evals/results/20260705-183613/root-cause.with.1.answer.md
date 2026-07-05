The issue is that `formatPrice` doesn't guard against `null` or `NaN` values. When a product has `priceCents: null`, arithmetic operations can produce `NaN`, which then gets formatted as the string `"$NaN"`.

The fix is to handle these edge cases in `formatPrice`:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null || isNaN(cents)) {
    return `$0.00`;
  }
  return `$${(cents / 100).toFixed(2)}`;
}
```

This defensive check ensures that `null` prices or any `NaN` results from cart calculations display as `$0.00` instead of `$NaN`, preventing the display bug regardless of where invalid values come from upstream.
