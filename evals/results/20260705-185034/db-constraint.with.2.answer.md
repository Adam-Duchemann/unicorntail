Add a unique constraint at the database level:

```sql
alter table public.albums 
add constraint albums_owner_id_name_unique unique(owner_id, name);
```

Update your create function to include `owner_id`:

```ts
export async function createAlbum(name: string) {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) throw new Error('Not authenticated');
  
  const { data, error } = await supabase
    .from('albums')
    .insert({ name, owner_id: user.id })
    .select()
    .single();
  
  if (error) {
    if (error.code === '23505') { // Unique violation
      throw new Error('You already have an album with that name');
    }
    throw error;
  }
  return data;
}
```

The constraint is atomic and prevents race conditions — this is better than a SELECT-then-INSERT check, which can fail under concurrent requests.
