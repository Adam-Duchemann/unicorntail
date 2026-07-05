Add a unique constraint on `(owner_id, name)` in the database:

```sql
alter table public.albums add constraint albums_owner_id_name_unique unique(owner_id, name);
```

Then update your TypeScript function to handle the constraint violation:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    // PostgreSQL error code 23505 = unique constraint violation
    if (error.code === '23505') {
      throw new Error('You already have an album with this name');
    }
    throw error;
  }
  
  return data;
}
```

The constraint prevents duplicates at the database layer (the only reliable place), and the app catches the error and surfaces a user-friendly message.
