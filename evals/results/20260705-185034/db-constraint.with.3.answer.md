Add a unique constraint on `(owner_id, name)` to the database:

```sql
alter table public.albums add constraint albums_owner_id_name_key unique(owner_id, name);
```

Then update your create function to handle the constraint violation:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') {
      throw new Error('You already have an album with this name');
    }
    throw error;
  }
  return data;
}
```

The `23505` code is Postgres's unique constraint violation. The constraint ensures one name per user (Postgres enforces uniqueness atomically at the database layer, preventing race conditions that app-side checks would miss).
