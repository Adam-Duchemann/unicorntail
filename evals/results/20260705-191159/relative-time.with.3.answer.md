Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  const rtf = new Intl.RelativeTimeFormat(locale);

  if (seconds < 60) return rtf.format(-seconds, 'second');
  if (seconds < 3600) return rtf.format(-Math.floor(seconds / 60), 'minute');
  if (seconds < 86400) return rtf.format(-Math.floor(seconds / 3600), 'hour');
  if (seconds < 604800) return rtf.format(-Math.floor(seconds / 86400), 'day');
  if (seconds < 2592000) return rtf.format(-Math.floor(seconds / 604800), 'week');
  if (seconds < 31536000) return rtf.format(-Math.floor(seconds / 2592000), 'month');
  return rtf.format(-Math.floor(seconds / 31536000), 'year');
}
```

Uses `Intl.RelativeTimeFormat` (built-in, locale-aware, handles all languages). The negative value indicates past tense.
