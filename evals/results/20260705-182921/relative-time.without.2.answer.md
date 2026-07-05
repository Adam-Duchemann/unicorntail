Add this function to your `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const then = new Date(iso);
  const seconds = Math.floor((now.getTime() - then.getTime()) / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (seconds < 60) {
    return rtf.format(-Math.round(seconds), 'second');
  } else if (seconds < 3600) {
    return rtf.format(-Math.round(seconds / 60), 'minute');
  } else if (seconds < 86400) {
    return rtf.format(-Math.round(seconds / 3600), 'hour');
  } else if (seconds < 604800) {
    return rtf.format(-Math.round(seconds / 86400), 'day');
  } else if (seconds < 2592000) {
    return rtf.format(-Math.round(seconds / 604800), 'week');
  } else if (seconds < 31536000) {
    return rtf.format(-Math.round(seconds / 2592000), 'month');
  } else {
    return rtf.format(-Math.round(seconds / 31536000), 'year');
  }
}
```

Use it like `formatTimeAgo(isoString, locale)`. It uses the built-in `Intl.RelativeTimeFormat` which handles locale-specific output and smart formatting (e.g., "yesterday" instead of "1 day ago" when appropriate).
