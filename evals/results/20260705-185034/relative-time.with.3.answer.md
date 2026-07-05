Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  const intervals: Array<[Intl.RelativeTimeFormatUnit, number]> = [
    ['year', 31536000],
    ['month', 2592000],
    ['week', 604800],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
    ['second', 1],
  ];
  
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  
  for (const [unit, secondsInUnit] of intervals) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return rtf.format(-interval, unit);
    }
  }
  
  return rtf.format(0, 'second');
}
```

Uses the native `Intl.RelativeTimeFormat` API—no dependency needed—which handles locale-aware formatting and edge cases like "today" vs "0 days ago" (via `numeric: 'auto'`).
