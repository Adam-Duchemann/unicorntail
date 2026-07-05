```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSecs = Math.floor(diffMs / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (diffSecs < 60) return rtf.format(-diffSecs, 'second');
  const diffMins = Math.floor(diffSecs / 60);
  if (diffMins < 60) return rtf.format(-diffMins, 'minute');
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return rtf.format(-diffHours, 'hour');
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return rtf.format(-diffDays, 'day');
  const diffWeeks = Math.floor(diffDays / 7);
  if (diffWeeks < 4) return rtf.format(-diffWeeks, 'week');
  const diffMonths = Math.floor(diffDays / 30);
  if (diffMonths < 12) return rtf.format(-diffMonths, 'month');
  const diffYears = Math.floor(diffDays / 365);
  return rtf.format(-diffYears, 'year');
}
```

Uses `Intl.RelativeTimeFormat` (no dependencies) to format relative times in the user's locale. The negative numbers represent "ago" (past time). Call it with the same ISO string and locale you'd pass to `formatDate`.
