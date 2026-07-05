Add a unique constraint on the combination of `owner_id` and `name`:

**SQL migration:**
```sql
alter table public.albums add constraint albums_owner_id_name_unique unique(owner_id, name);
```

**Updated TypeScript function:**
```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') {
      throw new Error(`You already have an album named "${name}"`);
    }
    throw error;
  }
  
  return data;
}
```

The database constraint prevents duplicates at the source and blocks race conditions. The error code `23505` is PostgreSQL's unique violation code — Supabase passes it through as-is.
