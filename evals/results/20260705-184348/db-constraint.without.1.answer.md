Add a unique constraint on the `(owner_id, name)` pair at the database level:

```sql
alter table public.albums add constraint albums_owner_id_name_key unique(owner_id, name);
```

Then handle the constraint violation in your app:

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

The database constraint prevents duplicate names per user at the source, and the app catches the unique violation error (PostgreSQL code 23505) to provide a user-friendly message.
