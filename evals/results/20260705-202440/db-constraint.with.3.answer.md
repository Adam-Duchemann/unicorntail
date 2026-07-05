Add a unique constraint to the database:

```sql
ALTER TABLE public.albums ADD CONSTRAINT unique_name_per_owner UNIQUE(owner_id, name);
```

Or if creating the table fresh:

```sql
create table public.albums (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id),
  name text not null,
  created_at timestamptz default now(),
  unique(owner_id, name)
);
```

Update the TypeScript function to handle the constraint violation:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') { // PostgreSQL unique constraint violation
      throw new Error('An album with this name already exists');
    }
    throw error;
  }
  return data;
}
```

This enforces uniqueness atomically at the database level, preventing race conditions where two simultaneous requests could both pass app-side checks.
