Enforce it with a partial unique index in Postgres (case-insensitive per owner), then map the resulting error code in your insert function.

**Migration:**

```sql
create unique index albums_owner_name_unique
  on public.albums (owner_id, lower(name));
```

**App-side function:**

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') {
      throw new Error('You already have an album with that name.');
    }
    throw error;
  }
  return data;
}
```

The unique index is the actual enforcement — atomic at the DB level, so it holds even under concurrent inserts. The `23505` check just turns the constraint violation into a friendly error instead of a raw Postgres error leaking to the caller.
