The issue is that `formatPrice` doesn't handle `null` values. When `cents` is `null`, arithmetic operations can result in `NaN`.

The fix is to handle the `null` case in `formatPrice`:

```js
// pricing.js — shared
export function formatPrice(cents) {
  const amount = cents ?? 0;
  return `$${(amount / 100).toFixed(2)}`;
}
```

The nullish coalescing operator (`??`) treats `null` and `undefined` as falsy and defaults to `0`, while still allowing legitimate `$0.00` prices (where `cents` is actually `0`). This displays unpriced items as "$0.00" across checkout, cart, and email receipt.
