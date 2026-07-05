My app uses Supabase (Postgres). Users must not be able to create two albums with the same name. Relevant table:

```sql
create table public.albums (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id),
  name text not null,
  created_at timestamptz default now()
);
```

App-side create function (TypeScript):

```ts
export async function createAlbum(name: string) {
  const { data, error } = await supabase.from('albums').insert({ name }).select().single();
  if (error) throw error;
  return data;
}
```

How do I enforce "no duplicate album names per user"? Reply with the code directly. Do not create files.
