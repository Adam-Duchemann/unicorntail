**Migration (SQL):**
```sql
alter table public.albums 
add constraint albums_owner_name_unique unique(owner_id, name);
```

**Updated TypeScript function:**
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

The UNIQUE constraint at the database layer prevents race conditions where two simultaneous requests could both check for existence and both succeed in creating.
