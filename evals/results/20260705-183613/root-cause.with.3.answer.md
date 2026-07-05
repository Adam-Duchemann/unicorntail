Looking at the issue: when `priceCents` is `null`, the expression `null / 100` produces `NaN`, which then gets stringified to `"NaN"`.

The fix is to handle `null` in `formatPrice`:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return 'Price not set';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This prevents NaN from appearing on the checkout page and in emails. Items with unset prices will now show "Price not set" instead.

If you want to be stricter (prevent null-priced items from being checkable in the first place), you'd also want to filter them out in the cart calculation, but this fix addresses the immediate bug.
