```html
<!-- Add this near the end of your body, before any scripts -->
<dialog id="deleteConfirmDialog">
  <p>This action cannot be undone.</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end;">
    <button onclick="document.getElementById('deleteConfirmDialog').close()">Cancel</button>
    <button id="confirmDeleteBtn" style="background-color: #dc2626; color: white;">Delete</button>
  </div>
</dialog>

<script>
  let pendingDeleteId = null;

  function showDeleteConfirm(id) {
    pendingDeleteId = id;
    document.getElementById('deleteConfirmDialog').showModal();
  }

  document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
    document.getElementById('deleteConfirmDialog').close();
    if (pendingDeleteId !== null) {
      deleteItem(pendingDeleteId);
      pendingDeleteId = null;
    }
  });
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

The `<dialog>` element handles modal behavior natively — it blocks interaction with the rest of the page and closes when you press Escape. Style the buttons as needed; the red background on Delete is just a suggestion.
