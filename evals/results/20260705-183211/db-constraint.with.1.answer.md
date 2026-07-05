**SQL migration:**

```sql
alter table public.albums
add constraint albums_owner_name_unique unique(owner_id, name);
```

**Updated TypeScript function:**

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') {
      // Unique constraint violation
      throw new Error(`An album named "${name}" already exists.`);
    }
    throw error;
  }
  
  return data;
}
```

The constraint prevents duplicate names per user at the database level. The `owner_id` is automatically set by an RLS policy or database trigger (add one if missing). Error code `23505` is Postgres's unique violation; catch it to show a user-friendly message.
