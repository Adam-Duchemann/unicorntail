**SQL (add to a migration or run directly):**

```sql
alter table public.albums 
add constraint albums_owner_id_name_unique unique(owner_id, name);
```

**TypeScript:**

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase
    .from('albums')
    .insert({ name })
    .select()
    .single();
  
  if (error) {
    if (error.code === '23505') { // unique constraint violation
      throw new Error('You already have an album with this name');
    }
    throw error;
  }
  return data;
}
```

The unique constraint on `(owner_id, name)` prevents duplicates per user at the database layer. Error code `23505` is Postgres's unique violation — catch it and translate to user-friendly messaging.
