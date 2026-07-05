Add a UNIQUE constraint on `(owner_id, name)` at the database level:

**Migration:**
```sql
alter table public.albums add constraint albums_owner_id_name_unique unique (owner_id, name);
```

**Updated TypeScript:**
```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') { // unique constraint violation
      throw new Error('You already have an album with this name');
    }
    throw error;
  }
  return data;
}
```

The constraint is enforced atomically at the database level — no race conditions, no app-side logic to bypass. The `23505` error code is Postgres's standard for unique constraint violations.
