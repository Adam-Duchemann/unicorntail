Add a unique constraint on `(owner_id, name)` at the database level, then handle the constraint violation error in your app.

**SQL migration** (add to `supabase/migrations/`):
```sql
alter table public.albums
  add constraint albums_owner_id_name_unique unique(owner_id, name);
```

**Updated TypeScript function:**
```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    // Postgres unique constraint violation
    if (error.code === '23505') {
      throw new Error('You already have an album with this name');
    }
    throw error;
  }
  return data;
}
```

The database constraint is the enforcement layer; the app-side error handling just translates the Postgres error code (`23505`) into a user-friendly message. Make sure `owner_id` is being set by your RLS policy or server-side logic—the constraint will only work if that column is populated.
