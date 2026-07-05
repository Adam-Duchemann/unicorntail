Add this dialog element to your HTML:

```html
<dialog id="confirmDialog" style="border: none; border-radius: 8px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <p style="margin: 0 0 24px 0; font-size: 16px;">This action cannot be undone</p>
  <div style="display: flex; gap: 12px; justify-content: flex-end;">
    <button id="cancelBtn" style="padding: 8px 16px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px; cursor: pointer;">Cancel</button>
    <button id="deleteBtn" style="padding: 8px 16px; background: #d32f2f; color: white; border: none; border-radius: 4px; cursor: pointer;">Delete</button>
  </div>
</dialog>
```

Replace your delete button's `onclick` with:

```html
<button onclick="showDeleteConfirm(itemId)">Delete</button>
```

Add this JavaScript:

```javascript
const dialog = document.getElementById('confirmDialog');
const cancelBtn = document.getElementById('cancelBtn');
const deleteBtn = document.getElementById('deleteBtn');
let pendingDeleteId = null;

function showDeleteConfirm(id) {
  pendingDeleteId = id;
  dialog.showModal();
}

cancelBtn.addEventListener('click', () => {
  dialog.close();
});

deleteBtn.addEventListener('click', () => {
  deleteItem(pendingDeleteId);
  dialog.close();
});
```

The `<dialog>` element is native HTML—no libraries needed. Clicking Delete runs `deleteItem()`, Cancel closes the dialog. You can customize the styling inline as shown.
