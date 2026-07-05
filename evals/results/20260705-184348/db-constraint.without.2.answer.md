**Database constraint** — add a unique index on `(owner_id, name)`:

```sql
alter table public.albums
add constraint albums_owner_id_name_unique unique (owner_id, name);
```

**App-side function** — capture the current user and include `owner_id`:

```ts
export async function createAlbum(name: string) {
  const { data: { user }, error: userError } = await supabase.auth.getUser();
  if (userError || !user) throw userError;

  const { data, error } = await supabase
    .from('albums')
    .insert({ name, owner_id: user.id })
    .select()
    .single();
  if (error) throw error;
  return data;
}
```

If a user tries to create a duplicate, the insert will fail with a unique constraint violation and `error` will be set. Handle it as needed (e.g., show "Album name already exists").
