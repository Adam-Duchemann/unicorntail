```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-seconds, 'second');
  }
  
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-minutes, 'minute');
  }
  
  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-hours, 'hour');
  }
  
  const days = Math.floor(hours / 24);
  if (days < 7) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-days, 'day');
  }
  
  const weeks = Math.floor(days / 7);
  if (weeks < 4) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-weeks, 'week');
  }
  
  const months = Math.floor(days / 30);
  if (months < 12) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-months, 'month');
  }
  
  const years = Math.floor(days / 365);
  return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-years, 'year');
}
```

Uses `Intl.RelativeTimeFormat` (same standard API as your `toLocaleDateString`). The `numeric: 'auto'` option produces natural phrasing like "yesterday" and "last week" where appropriate.
