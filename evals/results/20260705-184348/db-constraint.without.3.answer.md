Add a unique constraint on the (owner_id, name) pair, then handle the error in your app:

**Database (migration):**
```sql
ALTER TABLE public.albums 
ADD CONSTRAINT albums_owner_id_name_key UNIQUE (owner_id, name);
```

**TypeScript:**
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

The constraint ensures no two albums with the same name can exist for the same owner. The app catches the unique violation error (Postgres code `23505`) and surfaces a user-friendly message.
