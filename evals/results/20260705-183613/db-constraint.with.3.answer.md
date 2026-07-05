Add a UNIQUE constraint at the database level:

```sql
alter table public.albums add constraint unique_album_name_per_user unique(owner_id, name);
```

Update the app function to handle the constraint violation:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  
  if (error) {
    // PostgreSQL unique constraint violation
    if (error.code === '23505') {
      throw new Error('You already have an album with that name');
    }
    throw error;
  }
  
  return data;
}
```

The constraint ensures Postgres rejects duplicates atomically before the insert completes. The app catches the error and surfaces a user-friendly message.
