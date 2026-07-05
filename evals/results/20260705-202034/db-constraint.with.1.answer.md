Add a unique constraint on `(owner_id, name)` and let Postgres enforce it atomically — don't do a check-then-insert in app code, that's a race.

```sql
alter table public.albums
  add constraint albums_owner_id_name_key unique (owner_id, name);
```

Then update the app code to catch the constraint violation (Postgres error code `23505`) and surface a clear error:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') throw new Error('You already have an album with that name.');
    throw error;
  }
  return data;
}
```

Note: this is exact-match uniqueness. If you want "My Trip" and "my trip" to collide too, say so and I'll switch it to a unique index on `lower(name)` instead.
