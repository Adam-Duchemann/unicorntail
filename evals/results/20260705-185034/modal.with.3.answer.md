```html
<dialog id="deleteConfirm">
  <div style="min-width: 300px;">
    <p>This action cannot be undone</p>
    <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px;">
      <button onclick="document.getElementById('deleteConfirm').close()">Cancel</button>
      <button id="deleteConfirmBtn" style="background-color: #d32f2f; color: white;">Delete</button>
    </div>
  </div>
</dialog>

<script>
  let pendingDeleteId = null;

  function openDeleteConfirm(id) {
    pendingDeleteId = id;
    document.getElementById('deleteConfirm').showModal();
  }

  document.getElementById('deleteConfirmBtn').addEventListener('click', () => {
    if (pendingDeleteId !== null) {
      deleteItem(pendingDeleteId);
      document.getElementById('deleteConfirm').close();
      pendingDeleteId = null;
    }
  });
</script>
```

**Update your delete button:**
```html
<button onclick="openDeleteConfirm(id)">Delete</button>
```

The `<dialog>` element handles backdrop clicking and Escape key automatically (closes without deleting). The `showModal()` call makes it modal with a semi-transparent backdrop. Update the button colors/styles to match your design.
