**SQL — add a unique constraint on (owner_id, name):**

```sql
ALTER TABLE public.albums 
ADD CONSTRAINT albums_owner_id_name_key UNIQUE (owner_id, name);
```

**TypeScript — handle the duplicate error:**

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
      throw new Error('You already have an album with this name');
    }
    throw error;
  }
  return data;
}
```

The constraint prevents duplicates at the database level. The error code `23505` is PostgreSQL's unique violation code — Supabase passes it through, so you can detect and surface it as a friendly error to the user.
