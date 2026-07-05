**SQL migration** (add this constraint):

```sql
alter table public.albums
add constraint albums_owner_name_unique unique(owner_id, name);
```

**Updated TypeScript** (handle the duplicate error):

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') { // unique constraint violation
      throw new Error(`Album "${name}" already exists`);
    }
    throw error;
  }
  
  return data;
}
```

The unique constraint on `(owner_id, name)` prevents duplicates per user at the database level — no two rows can have the same owner_id and name. The app catches the 23505 error (PostgreSQL's unique violation code) and translates it to a user-friendly message.
