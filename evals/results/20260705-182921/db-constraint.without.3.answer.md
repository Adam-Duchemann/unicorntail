Add a unique constraint on `(owner_id, name)`:

**Migration (SQL):**
```sql
alter table public.albums
add constraint albums_owner_name_unique unique(owner_id, name);
```

**TypeScript update (handle the constraint violation):**
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

The unique constraint enforces it at the database level (reliable, no race conditions), and the app catches the Postgres error code `23505` (unique constraint violation) to return a user-friendly message. Since `owner_id` is already set by your auth context (add it to the insert), the constraint prevents duplicates per user without allowing the same name across different users.
