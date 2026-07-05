The bug occurs because `formatPrice` doesn't handle `null` values. When `cents` is `null`, dividing it produces `NaN`.

**Fix for `pricing.js`:**

```js
export function formatPrice(cents) {
  return `$${((cents ?? 0) / 100).toFixed(2)}`;
}
```

**Additional fix for `cartTotalCents` (not shown but likely needed):**

If `cartTotalCents` is something like:
```js
function cartTotalCents(items) {
  return items.reduce((sum, item) => sum + item.priceCents, 0);
}
```

It should be:
```js
function cartTotalCents(items) {
  return items.reduce((sum, item) => sum + (item.priceCents ?? 0), 0);
}
```

The `??` operator treats `null` as 0, so items without prices display as $0.00 instead of NaN.
