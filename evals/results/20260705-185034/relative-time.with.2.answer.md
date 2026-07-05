Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
  const diffMs = now.getTime() - date.getTime();

  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;
  const week = 7 * day;
  const month = 30 * day;
  const year = 365 * day;

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (diffMs < minute) return rtf.format(-Math.round(diffMs / 1000), 'second');
  if (diffMs < hour) return rtf.format(-Math.round(diffMs / minute), 'minute');
  if (diffMs < day) return rtf.format(-Math.round(diffMs / hour), 'hour');
  if (diffMs < week) return rtf.format(-Math.round(diffMs / day), 'day');
  if (diffMs < month) return rtf.format(-Math.round(diffMs / week), 'week');
  if (diffMs < year) return rtf.format(-Math.round(diffMs / month), 'month');
  return rtf.format(-Math.round(diffMs / year), 'year');
}
```

Uses `Intl.RelativeTimeFormat` to handle localization automatically — produces "3 minutes ago", "2 days ago", "yesterday", etc. in the user's language. Works in all modern browsers.
