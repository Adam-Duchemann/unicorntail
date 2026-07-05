**SQL constraint** (add to your migration or run directly):

```sql
alter table public.albums
  add constraint unique_owner_album_name unique(owner_id, name);
```

**Updated TypeScript function** (handles constraint violation):

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase
    .from('albums')
    .insert({ name })
    .select()
    .single();
  
  if (error) {
    if (error.code === '23505') {
      throw new Error('You already have an album with that name');
    }
    throw error;
  }
  
  return data;
}
```

The constraint lives at the database layer (preventing duplicates even if the app has a bug), and the app catches PostgreSQL's `23505` (unique_violation) error code to return a user-friendly message.
