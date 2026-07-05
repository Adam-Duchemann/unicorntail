**SQL migration** — add a unique constraint on (owner_id, name):

```sql
alter table public.albums
add constraint albums_owner_id_name_key unique(owner_id, name);
```

**Updated TypeScript** — pass owner_id explicitly:

```ts
export async function createAlbum(name: string) {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) throw new Error('Not authenticated');
  
  const { data, error } = await supabase
    .from('albums')
    .insert({ name, owner_id: user.id })
    .select()
    .single();
  
  if (error) throw error;
  return data;
}
```

If the duplicate is attempted, Supabase will return a 409 conflict error in the `error` object, which you can handle as needed.
