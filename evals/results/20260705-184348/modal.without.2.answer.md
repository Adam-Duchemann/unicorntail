```html
<!-- Add this to your HTML -->
<dialog id="deleteConfirmDialog">
  <div style="padding: 20px; font-family: sans-serif;">
    <p style="margin-top: 0;">This action cannot be undone</p>
    <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
      <button id="cancelBtn" style="padding: 8px 16px;">Cancel</button>
      <button id="deleteBtn" style="padding: 8px 16px; background: #dc2626; color: white; border: none; border-radius: 4px; cursor: pointer;">Delete</button>
    </div>
  </div>
</dialog>

<!-- Update your delete button to call showDeleteConfirm instead -->
<button onclick="showDeleteConfirm(123)">Delete Item</button>
```

```javascript
let pendingDeleteId = null;

function showDeleteConfirm(id) {
  pendingDeleteId = id;
  document.getElementById('deleteConfirmDialog').showModal();
}

document.getElementById('deleteBtn').addEventListener('click', () => {
  document.getElementById('deleteConfirmDialog').close();
  deleteItem(pendingDeleteId);
  pendingDeleteId = null;
});

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('deleteConfirmDialog').close();
  pendingDeleteId = null;
});
```

Replace `123` with your actual item ID. The `<dialog>` element is supported in all modern browsers and automatically handles the modal overlay and focus management.
