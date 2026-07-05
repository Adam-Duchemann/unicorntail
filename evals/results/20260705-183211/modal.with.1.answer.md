Here's the code using the native `<dialog>` element:

**HTML (add to your page):**
```html
<dialog id="deleteConfirmDialog">
  <div style="padding: 20px; min-width: 300px;">
    <p style="margin: 0 0 20px 0;">This action cannot be undone</p>
    <div style="display: flex; gap: 10px; justify-content: flex-end;">
      <button onclick="document.getElementById('deleteConfirmDialog').close('cancel')">Cancel</button>
      <button onclick="document.getElementById('deleteConfirmDialog').close('delete')" style="background: #d32f2f; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">Delete</button>
    </div>
  </div>
</dialog>
```

**JavaScript:**
```javascript
async function handleDelete(id) {
  const dialog = document.getElementById('deleteConfirmDialog');
  dialog.returnValue = '';
  dialog.showModal();
  
  const result = await new Promise(resolve => {
    dialog.addEventListener('close', () => resolve(dialog.returnValue), { once: true });
  });
  
  if (result === 'delete') {
    deleteItem(id);
  }
}
```

**Update your delete button to:**
```html
<button onclick="handleDelete(123)">Delete</button>
```

The dialog blocks interaction with the rest of the page until dismissed. Cancel or clicking outside closes it without deleting.
