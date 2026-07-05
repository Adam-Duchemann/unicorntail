Enforce it at the database level with a unique constraint — an app-side check-then-insert is a race (two requests can pass the check simultaneously).

```sql
create unique index albums_owner_id_name_key
  on public.albums (owner_id, name);
```

Then update `createAlbum` to require the caller pass `owner_id` (it's not nullable, so it must be set explicitly — RLS/insert won't infer it) and translate the constraint violation into a clean error:

```ts
export async function createAlbum(ownerId: string, name: string) {
  const { data, error } = await supabase
    .from('albums')
    .insert({ owner_id: ownerId, name })
    .select()
    .single();

  if (error) {
    if (error.code === '23505') {
      throw new Error(`You already have an album named "${name}".`);
    }
    throw error;
  }

  return data;
}
```

`23505` is Postgres's unique_violation code, passed through by PostgREST/supabase-js in `error.code`.
