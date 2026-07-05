Add this function to your `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-Math.round(seconds), 'second');
  }

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-Math.round(minutes), 'minute');
  }

  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-Math.round(hours), 'hour');
  }

  const days = Math.floor(hours / 24);
  if (days < 30) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-Math.round(days), 'day');
  }

  const months = Math.floor(days / 30);
  if (months < 12) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-Math.round(months), 'month');
  }

  const years = Math.floor(months / 12);
  return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-Math.round(years), 'year');
}
```

Use it like: `formatTimeAgo(isoString, 'fr')` → `"il y a 3 minutes"` (in French), `formatTimeAgo(isoString, 'en')` → `"3 minutes ago"` (in English). `numeric: 'auto'` produces natural forms like "yesterday" or "last year" when appropriate.
