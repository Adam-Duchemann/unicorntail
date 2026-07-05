**SQL (add to a migration file):**

```sql
alter table public.albums add constraint albums_owner_name_unique unique (owner_id, name);
```

**TypeScript (updated function):**

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    if (error.code === '23505') {
      throw new Error(`Album "${name}" already exists`);
    }
    throw error;
  }
  
  return data;
}
```

The unique constraint on `(owner_id, name)` ensures each user can only have one album with a given name. The `23505` error code is Postgres's unique-violation code. Without the app-side check, you'll still be protected by the DB constraint—the check just gives a friendlier error message.
