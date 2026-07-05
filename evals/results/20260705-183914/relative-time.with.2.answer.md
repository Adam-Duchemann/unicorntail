Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
  const diffMs = now.getTime() - date.getTime();
  const diffSeconds = Math.floor(diffMs / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (diffSeconds < 60) return rtf.format(-diffSeconds, 'second');
  const minutes = Math.floor(diffSeconds / 60);
  if (minutes < 60) return rtf.format(-minutes, 'minute');
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return rtf.format(-hours, 'hour');
  const days = Math.floor(hours / 24);
  if (days < 7) return rtf.format(-days, 'day');
  const weeks = Math.floor(days / 7);
  if (weeks < 4) return rtf.format(-weeks, 'week');
  const months = Math.floor(days / 30);
  if (months < 12) return rtf.format(-months, 'month');
  const years = Math.floor(months / 12);
  return rtf.format(-years, 'year');
}
```

Uses `Intl.RelativeTimeFormat` (built-in, no dependency) to format relative times in any locale. Pass the ISO date and locale string; it picks the right unit and returns localized "X time ago" text.
