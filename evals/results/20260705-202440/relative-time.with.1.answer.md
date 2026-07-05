Add this function to `src/utils/date.ts`:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const past = new Date(iso);
  const secondsAgo = Math.floor((now.getTime() - past.getTime()) / 1000);
  
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  
  if (secondsAgo < 60) {
    return rtf.format(-secondsAgo, 'second');
  } else if (secondsAgo < 3600) {
    return rtf.format(-Math.floor(secondsAgo / 60), 'minute');
  } else if (secondsAgo < 86400) {
    return rtf.format(-Math.floor(secondsAgo / 3600), 'hour');
  } else if (secondsAgo < 2592000) {
    return rtf.format(-Math.floor(secondsAgo / 86400), 'day');
  } else if (secondsAgo < 31536000) {
    return rtf.format(-Math.floor(secondsAgo / 2592000), 'month');
  } else {
    return rtf.format(-Math.floor(secondsAgo / 31536000), 'year');
  }
}
```

Uses the native [`Intl.RelativeTimeFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat) API to handle all localization—it automatically produces "3 minutes ago", "il y a 3 minutes", etc. depending on locale. The `numeric: 'auto'` option makes it say "yesterday" instead of "1 day ago" for better readability.
