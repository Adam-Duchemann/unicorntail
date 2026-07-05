The bug is in `formatPrice` — it doesn't guard against `null`. When `cents` is `null`, `null / 100` becomes `NaN`.

```js
export function formatPrice(cents) {
  return `$${((cents ?? 0) / 100).toFixed(2)}`;
}
```

This treats missing prices as $0.00, fixing NaN in checkout, cart, and email-receipt in one place.
