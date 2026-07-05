Add a unique constraint in Postgres (enforced atomically at the DB layer — an app-side check-then-insert would race), then catch the violation in your function.

**Migration:**
```sql
alter table public.albums
  add constraint albums_owner_id_name_key unique (owner_id, name);
```

If you want case-insensitive matching ("Trip" and "trip" count as duplicates), use a unique index instead:
```sql
create unique index albums_owner_id_name_ci_key on public.albums (owner_id, lower(name));
```

**Updated function** (catch Postgres unique-violation code `23505` for a clean error):
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
