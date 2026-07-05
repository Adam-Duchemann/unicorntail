**Database constraint** (add to your Supabase migration):

```sql
alter table public.albums add constraint albums_owner_id_name_key unique(owner_id, name);
```

**TypeScript client** (updated `createAlbum`):

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') { // unique constraint violation
      throw new Error(`You already have an album named "${name}"`);
    }
    throw error;
  }
  
  return data;
}
```

The `unique(owner_id, name)` constraint prevents duplicates per user at the database level. The error code `23505` is PostgreSQL's unique violation; catching it lets you provide a user-friendly message instead of a raw DB error.
