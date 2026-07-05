Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
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
  if (days < 30) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-days, 'day');
  }
  
  const months = Math.floor(days / 30);
  if (months < 12) {
    return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-months, 'month');
  }
  
  const years = Math.floor(months / 12);
  return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-years, 'year');
}
```

Uses the native `Intl.RelativeTimeFormat` API — no dependencies, automatically localizes to the user's language, and produces natural output like "3 minutes ago", "2 days ago", "now", etc. depending on the locale.
