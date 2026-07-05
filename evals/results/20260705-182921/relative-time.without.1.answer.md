Add this function to `src/utils/date.ts`:

```ts
export function timeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return 'just now';

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  
  if (seconds < 3600) {
    return rtf.format(-Math.floor(seconds / 60), 'minute');
  }
  if (seconds < 86400) {
    return rtf.format(-Math.floor(seconds / 3600), 'hour');
  }
  if (seconds < 604800) {
    return rtf.format(-Math.floor(seconds / 86400), 'day');
  }
  if (seconds < 2592000) {
    return rtf.format(-Math.floor(seconds / 604800), 'week');
  }
  if (seconds < 31536000) {
    return rtf.format(-Math.floor(seconds / 2592000), 'month');
  }
  
  return rtf.format(-Math.floor(seconds / 31536000), 'year');
}
```

Uses `Intl.RelativeTimeFormat` for automatic locale-aware formatting with smart rounding (e.g., "yesterday" instead of "1 day ago"). Pass an ISO string and locale code: `timeAgo("2026-07-01T00:00:00Z", "fr")` → "4 days ago" (or equivalent in French).
