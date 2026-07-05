In my TypeScript web app I need to show "time ago" style timestamps ("3 minutes ago", "2 days ago") for feed items, in the user's language (the app already knows the locale string, e.g. "fr").

My existing `src/utils/date.ts` already contains:

```ts
export function formatDate(iso: string, locale: string): string {
  return new Date(iso).toLocaleDateString(locale, { dateStyle: 'medium' });
}
```

What do I add? Reply with the code directly. Do not create files.
