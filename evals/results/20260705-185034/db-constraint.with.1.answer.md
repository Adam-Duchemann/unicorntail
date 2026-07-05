Add a UNIQUE constraint on `(owner_id, name)` to the database:

```sql
ALTER TABLE public.albums
ADD CONSTRAINT albums_owner_id_name_unique UNIQUE (owner_id, name);
```

Then update the app-side function to capture the current user's ID:

```ts
export async function createAlbum(name: string) {
  const { data: { user }, error: authError } = await supabase.auth.getUser();
  if (authError || !user) throw new Error('Not authenticated');
  
  const { data, error } = await supabase
    .from('albums')
    .insert({ name, owner_id: user.id })
    .select()
    .single();
  
  if (error) throw error;
  return data;
}
```

The Postgres constraint will reject duplicate inserts with a unique violation error (caught by the `if (error)` block). This prevents race conditions where two concurrent requests might both pass app-side checks.
