```html
<dialog id="confirmDelete">
  <p>This action cannot be undone</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end;">
    <button onclick="document.getElementById('confirmDelete').close()">Cancel</button>
    <button onclick="confirmDeleteAction()">Delete</button>
  </div>
</dialog>

<script>
  let pendingDeleteId = null;

  function showDeleteConfirm(id) {
    pendingDeleteId = id;
    document.getElementById('confirmDelete').showModal();
  }

  function confirmDeleteAction() {
    if (pendingDeleteId !== null) {
      deleteItem(pendingDeleteId);
      document.getElementById('confirmDelete').close();
      pendingDeleteId = null;
    }
  }
</script>
```

Then change your delete button from:
```html
<button onclick="deleteItem(id)">Delete</button>
```

To:
```html
<button onclick="showDeleteConfirm(id)">Delete</button>
```

The `<dialog>` element handles the modal overlay, focus trapping, and dismissal via Escape automatically. `showModal()` makes it fullscreen modal; `.close()` dismisses it.
