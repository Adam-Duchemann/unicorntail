```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (seconds < 60) return rtf.format(-seconds, 'second');
  if (seconds < 3600) return rtf.format(-Math.floor(seconds / 60), 'minute');
  if (seconds < 86400) return rtf.format(-Math.floor(seconds / 3600), 'hour');
  if (seconds < 604800) return rtf.format(-Math.floor(seconds / 86400), 'day');
  if (seconds < 2592000) return rtf.format(-Math.floor(seconds / 604800), 'week');
  if (seconds < 31536000) return rtf.format(-Math.floor(seconds / 2592000), 'month');
  return rtf.format(-Math.floor(seconds / 31536000), 'year');
}
```

Add this to your `src/utils/date.ts`. It uses `Intl.RelativeTimeFormat` (native browser API) to handle locale-specific "ago" formatting automatically — e.g., with `numeric: 'auto'`, it shows "yesterday" instead of "1 day ago" for recent dates. Call it with the same locale string you use elsewhere.
