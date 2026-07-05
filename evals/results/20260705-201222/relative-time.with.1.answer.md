Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const then = new Date(iso);
  const diffMs = now.getTime() - then.getTime();
  const diffSecs = Math.floor(diffMs / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (diffSecs < 60) return rtf.format(0, 'second');
  const mins = Math.floor(diffSecs / 60);
  if (mins < 60) return rtf.format(-mins, 'minute');
  const hours = Math.floor(diffSecs / 3600);
  if (hours < 24) return rtf.format(-hours, 'hour');
  const days = Math.floor(diffSecs / 86400);
  if (days < 7) return rtf.format(-days, 'day');
  const weeks = Math.floor(diffSecs / 604800);
  if (weeks < 4) return rtf.format(-weeks, 'week');
  const months = Math.floor(diffSecs / 2592000);
  if (months < 12) return rtf.format(-months, 'month');
  const years = Math.floor(diffSecs / 31536000);
  return rtf.format(-years, 'year');
}
```

Uses the native `Intl.RelativeTimeFormat` API to handle all the localization automatically. Call it with `formatTimeAgo(isoString, locale)` and it returns "3 minutes ago", "2 days ago", etc. in the correct language.
