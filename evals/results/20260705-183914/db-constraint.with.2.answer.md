**SQL migration** (add to a new Supabase migration):

```sql
alter table public.albums add constraint albums_owner_name_unique unique (owner_id, name);
```

**Updated TypeScript** (handle the constraint violation):

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') { // postgres unique violation
      throw new Error(`Album "${name}" already exists`);
    }
    throw error;
  }
  
  return data;
}
```

The unique constraint on `(owner_id, name)` is atomic and prevents duplicates at the database layer, so no SELECT-then-INSERT race condition. The error code `23505` is Postgres's standard unique violation code.
