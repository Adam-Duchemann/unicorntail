```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}

// checkout.js
function cartTotalCents(items) {
  return items.reduce((sum, item) => sum + (item.priceCents ?? 0), 0);
}

summary.total = formatPrice(cartTotalCents(items));
```

The issue: `formatPrice()` receives `null` from products with unset prices, and `cartTotalCents()` (which you call but wasn't shown) needs to handle `null` values when summing. The fix treats missing prices as 0 in both places.
