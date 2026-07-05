```html
<!-- Add this dialog to your HTML -->
<dialog id="deleteDialog">
  <p>This action cannot be undone</p>
  <div>
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn">Delete</button>
  </div>
</dialog>

<!-- Your delete button stays the same -->
<button onclick="openDeleteDialog(itemId)">Delete</button>
```

```javascript
let pendingDeleteId = null;

function openDeleteDialog(id) {
  pendingDeleteId = id;
  document.getElementById('deleteDialog').showModal();
}

document.getElementById('cancelBtn').onclick = () => {
  document.getElementById('deleteDialog').close();
  pendingDeleteId = null;
};

document.getElementById('confirmDeleteBtn').onclick = () => {
  document.getElementById('deleteDialog').close();
  deleteItem(pendingDeleteId);
  pendingDeleteId = null;
};
```

Optional minimal styling:
```css
dialog {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  max-width: 400px;
}

dialog > div {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 15px;
}

dialog button {
  padding: 8px 16px;
  cursor: pointer;
}
```

The `<dialog>` element is native to all modern browsers — no library needed. `.showModal()` adds a backdrop, `.close()` dismisses it. Press Escape to cancel.
