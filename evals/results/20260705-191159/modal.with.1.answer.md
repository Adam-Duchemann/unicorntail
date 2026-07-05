**Native confirm (simplest):**

```javascript
function confirmDelete(id) {
  if (confirm("This action cannot be undone")) {
    deleteItem(id);
  }
}
```

Then change your delete button:
```html
<button onclick="confirmDelete(id)">Delete</button>
```

---

**Custom modal (if you want styled buttons):**

```html
<div id="deleteModal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
  <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <p style="margin: 0 0 20px 0;">This action cannot be undone</p>
    <div style="display: flex; gap: 10px; justify-content: flex-end;">
      <button onclick="closeDeleteModal()">Cancel</button>
      <button onclick="confirmDeleteItem()" style="background: #dc2626; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Delete</button>
    </div>
  </div>
</div>

<script>
let deleteId = null;

function showDeleteModal(id) {
  deleteId = id;
  document.getElementById("deleteModal").style.display = "flex";
}

function closeDeleteModal() {
  deleteId = null;
  document.getElementById("deleteModal").style.display = "none";
}

function confirmDeleteItem() {
  if (deleteId !== null) {
    deleteItem(deleteId);
    closeDeleteModal();
  }
}
</script>
```

Then change your delete button:
```html
<button onclick="showDeleteModal(id)">Delete</button>
```

Pick native `confirm()` unless you need to style the buttons — native is bulletproof and zero CSS.
