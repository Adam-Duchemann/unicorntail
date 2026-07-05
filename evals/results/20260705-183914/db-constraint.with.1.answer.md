Add a unique composite constraint at the database level:

**SQL Migration:**
```sql
alter table public.albums
add constraint albums_owner_name_unique unique(owner_id, name);
```

**Updated TypeScript:**
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
    if (error.code === '23505') {
      throw new Error('Album with this name already exists');
    }
    throw error;
  }
  
  return data;
}
```

The composite unique constraint prevents duplicate names per user while allowing other users to have the same album name. Error code `23505` is Postgres's unique violation code.

**Note:** Your current code doesn't pass `owner_id` to insert, so every album would be owned by null. Make sure you're capturing the logged-in user's ID and sending it with each insert.
