Add a unique constraint at the database level (atomic, prevents race conditions):

```sql
alter table public.albums add constraint unique_album_name_per_user unique (owner_id, name);
```

Update your TypeScript to handle the constraint violation gracefully:

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) {
    if (error.code === '23505') { // postgres unique_violation
      throw new Error(`You already have an album named "${name}"`);
    }
    throw error;
  }
  return data;
}
```

The constraint lives in the database where it's atomic—no race window where two simultaneous requests both pass the check. The app code just surfaces a clear error message when it happens.
