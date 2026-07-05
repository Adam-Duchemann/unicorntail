No memory access granted, but this is self-contained — proceeding directly.

This needs to be enforced atomically at the DB layer (a `SELECT`-then-`INSERT` check in app code races). Add a unique constraint and handle the resulting error code:

```sql
create unique index albums_owner_id_name_key
  on public.albums (owner_id, name);
```

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') {
      throw new Error('You already have an album with this name.');
    }
    throw error;
  }
  return data;
}
```

Note: `createAlbum` doesn't take `owner_id` explicitly — insert must be populating it via a default/trigger (e.g. `default auth.uid()`) or RLS would reject it. If it's not currently set that way, add `owner_id: (await supabase.auth.getUser()).data.user.id` to the insert.

If names should be treated case-insensitively (`"Trip"` and `"trip"` counted as duplicates), use an expression index instead:

```sql
create unique index albums_owner_id_name_key
  on public.albums (owner_id, lower(name));
```
