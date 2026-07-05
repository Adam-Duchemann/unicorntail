Add a unique constraint to the database:

```sql
alter table public.albums
add constraint albums_owner_name_unique unique(owner_id, name);
```

Update the insert function to include the current user:

```ts
export async function createAlbum(name: string) {
  const { data: { user }, error: userError } = await supabase.auth.getUser();
  if (userError || !user) throw new Error('Not authenticated');
  
  const { data, error } = await supabase
    .from('albums')
    .insert({ name, owner_id: user.id })
    .select()
    .single();
  
  if (error) throw error;
  return data;
}
```

The constraint prevents duplicate names within each user. The function now captures the authenticated user's ID and includes it in the insert. If a duplicate occurs, Postgres rejects it with a constraint violation—handle that error however your app handles database errors.
