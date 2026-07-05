Two issues: the constraint needs to be per-`owner_id`, and `owner_id` currently isn't being set on insert (it'll fail the `not null` constraint regardless).

**Migration:**

```sql
alter table public.albums
  add constraint albums_owner_id_name_key unique (owner_id, name);
```

This is a DB-level constraint, so it's atomic — no race between a check and an insert.

**Updated create function** (sets `owner_id` from the authenticated user, and turns the constraint violation into a clear error):

```ts
export async function createAlbum(name: string) {
  const { data: userData, error: userError } = await supabase.auth.getUser();
  if (userError || !userData.user) throw userError ?? new Error('Not authenticated');

  const { data, error } = await supabase
    .from('albums')
    .insert({ name, owner_id: userData.user.id })
    .select()
    .single();

  if (error) {
    if (error.code === '23505') throw new Error(`Album "${name}" already exists`);
    throw error;
  }
  return data;
}
```

If you want same-name-different-case (`"Trip"` vs `"trip"`) blocked too, use a unique index on `(owner_id, lower(name))` instead and query/match accordingly — say so and I'll adjust.
