```js
export function formatPrice(cents) {
  if (cents == null) return "$0.00";
  return `$${(cents / 100).toFixed(2)}`;
}
```

The fix checks if `cents` is `null` or `undefined` before attempting the division. When a product has no price set, it returns `"$0.00"` instead of `"NaN"`. This handles the issue at the shared function level, fixing the bug across all call sites (cart, checkout, email-receipt).
