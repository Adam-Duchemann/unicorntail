Add this function to `src/utils/date.ts`. It uses the built-in `Intl.RelativeTimeFormat` API for automatic i18n support:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const diffMs = Date.now() - date.getTime();
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (diffMs < 60_000) return rtf.format(-Math.floor(diffMs / 1000), 'second');
  if (diffMs < 3_600_000) return rtf.format(-Math.floor(diffMs / 60_000), 'minute');
  if (diffMs < 86_400_000) return rtf.format(-Math.floor(diffMs / 3_600_000), 'hour');

  const diffDays = Math.floor(diffMs / 86_400_000);
  if (diffDays < 7) return rtf.format(-diffDays, 'day');
  if (diffDays < 30) return rtf.format(-Math.floor(diffDays / 7), 'week');
  if (diffDays < 365) return rtf.format(-Math.floor(diffDays / 30), 'month');
  return rtf.format(-Math.floor(diffDays / 365), 'year');
}
```

Call it with `formatTimeAgo(isoString, locale)` — it returns locale-aware strings like "3 minutes ago", "il y a 2 jours" (for French), etc.
