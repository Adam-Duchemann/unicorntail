Add a unique constraint on `(owner_id, name)` at the database level:

```sql
alter table public.albums
  add constraint albums_owner_id_name_unique unique(owner_id, name);
```

Update your TypeScript function to handle the duplicate error gracefully:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') { // unique_violation
      throw new Error(`You already have an album named "${name}"`);
    }
    throw error;
  }
  
  return data;
}
```

The database constraint prevents duplicates even under concurrent requests. The app-side error handling gives users a clear message instead of a generic database error.
