The bug occurs because `formatPrice` doesn't handle `null` values. When `cents` is `null`, dividing by 100 produces `NaN`.

**Fix:**

```js
// pricing.js — shared
export function formatPrice(cents) {
  return `$${((cents ?? 0) / 100).toFixed(2)}`;
}
```

This treats missing prices as `$0.00`. If you'd prefer to prevent items without prices from being checkable in the first place, that would require adding validation when items are added to the cart—but this one-line fix stops the NaN display.
