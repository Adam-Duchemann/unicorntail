Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  const intervals = [
    { name: 'year' as const, seconds: 31536000 },
    { name: 'month' as const, seconds: 2592000 },
    { name: 'week' as const, seconds: 604800 },
    { name: 'day' as const, seconds: 86400 },
    { name: 'hour' as const, seconds: 3600 },
    { name: 'minute' as const, seconds: 60 },
    { name: 'second' as const, seconds: 1 },
  ];

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      return rtf.format(-count, interval.name);
    }
  }

  return rtf.format(0, 'second');
}
```

It uses the built-in `Intl.RelativeTimeFormat` API to handle localization, and `numeric: 'auto'` produces natural phrases like "yesterday" or "2 hours ago" depending on the language.
