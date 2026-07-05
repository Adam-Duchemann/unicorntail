Add this function to your `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
  const diffMs = now.getTime() - date.getTime();
  const diffSeconds = Math.floor(diffMs / 1000);
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (diffSeconds < 60) {
    return rtf.format(-diffSeconds, 'second');
  }

  const diffMinutes = Math.floor(diffSeconds / 60);
  if (diffMinutes < 60) {
    return rtf.format(-diffMinutes, 'minute');
  }

  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) {
    return rtf.format(-diffHours, 'hour');
  }

  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) {
    return rtf.format(-diffDays, 'day');
  }

  const diffWeeks = Math.floor(diffDays / 7);
  if (diffWeeks < 4) {
    return rtf.format(-diffWeeks, 'week');
  }

  const diffMonths = Math.floor(diffDays / 30);
  if (diffMonths < 12) {
    return rtf.format(-diffMonths, 'month');
  }

  const diffYears = Math.floor(diffDays / 365);
  return rtf.format(-diffYears, 'year');
}
```

Uses the built-in `Intl.RelativeTimeFormat` API for proper localization. Pass `iso` (ISO date string) and `locale` (e.g., `"fr"`) and it returns "3 minutes ago", "il y a 3 minutes", etc. in the user's language.
