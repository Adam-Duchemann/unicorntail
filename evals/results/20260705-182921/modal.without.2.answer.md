Here's the simplest approach using the native browser confirm dialog:

```javascript
function deleteWithConfirmation(id) {
  if (confirm('This action cannot be undone')) {
    deleteItem(id);
  }
}
```

Then update your delete button to call this instead:
```html
<button onclick="deleteWithConfirmation(id)">Delete</button>
```

---

If you want a custom dialog with styled buttons, use this HTML dialog:

```html
<dialog id="deleteConfirmDialog" style="padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <p style="margin: 0 0 20px 0;">This action cannot be undone</p>
  <div style="display: flex; gap: 10px; justify-content: flex-end;">
    <button onclick="document.getElementById('deleteConfirmDialog').close()" style="padding: 8px 16px;">
      Cancel
    </button>
    <button id="confirmDeleteBtn" style="padding: 8px 16px; background: #d32f2f; color: white; border: none; border-radius: 4px; cursor: pointer;">
      Delete
    </button>
  </div>
</dialog>

<script>
function deleteWithConfirmation(id) {
  const dialog = document.getElementById('deleteConfirmDialog');
  const confirmBtn = document.getElementById('confirmDeleteBtn');
  
  confirmBtn.onclick = () => {
    dialog.close();
    deleteItem(id);
  };
  
  dialog.showModal();
}
</script>
```

Then call `deleteWithConfirmation(id)` from your delete button. The native `<dialog>` element handles the overlay and focus trapping automatically.
