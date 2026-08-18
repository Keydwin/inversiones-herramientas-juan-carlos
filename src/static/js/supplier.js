document.addEventListener('DOMContentLoaded', () => {
    // Modal controls for registration
    const openSupplierModalBtn = document.getElementById('openSupplierModalBtn');
    const SupplierModal = document.getElementById('SupplierModal');
    const closeSupplierBtn = document.getElementById('closeSupplierBtn');
    
    // Form inputs by ID
    const supplierInput = document.getElementById('NombreProveedor');
    const updateSupplierInput = document.getElementById('UpdateNombreProveedor');

    // Handle open/close modal action
    if (openSupplierModalBtn && SupplierModal && closeSupplierBtn) {
        openSupplierModalBtn.addEventListener('click', () => {
            const form = SupplierModal.querySelector('form');
            if (form) form.reset();
            SupplierModal.classList.add('active');
        });
        closeSupplierBtn.addEventListener('click', () => SupplierModal.classList.remove('active'));
    }

    // Direct restrictions for supplier name input (Register)
    if (supplierInput) {
        supplierInput.maxLength = 30;
        supplierInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 ]/g, '');
        });
    }

    // Direct restrictions for supplier name input (Update)
    if (updateSupplierInput) {
        updateSupplierInput.maxLength = 30;
        updateSupplierInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 ]/g, '');
        });
    }
});

// GLOBAL TABLES FUNCTIONS (PROVEEDORES)

// Open update modal and populate inputs with active row data
function openUpdateModal(id, nombre) {
    const UpdateSupplierModal = document.getElementById('UpdateSupplierModal');
    const UpdateSupplierForm = document.getElementById('UpdateSupplierForm');
    const closeUpdateSupplierBtn = document.getElementById('closeUpdateSupplierBtn');
    const UpdateNombreProveedor = document.getElementById('UpdateNombreProveedor');

    if (UpdateSupplierModal && UpdateSupplierForm && UpdateNombreProveedor && closeUpdateSupplierBtn) {
        UpdateSupplierForm.action = `/proveedores/update_supplier/${id}`;
        UpdateNombreProveedor.value = nombre;
        UpdateSupplierModal.classList.add('active');
        
        closeUpdateSupplierBtn.addEventListener('click', () => UpdateSupplierModal.classList.remove('active'));
    }
}

// Open delete modal and configure action URL
function openDeleteModal(id) {
    const DeleteSupplierModal = document.getElementById('DeleteSupplierModal');
    const DeleteSupplierForm = document.getElementById('DeleteSupplierForm');
    const closeDeleteSupplierBtn = document.getElementById('closeDeleteSupplierBtn');

    if (DeleteSupplierModal && DeleteSupplierForm && closeDeleteSupplierBtn) {
        DeleteSupplierForm.action = `/proveedores/delete_supplier/${id}`;
        DeleteSupplierModal.classList.add('active'); 
        
        closeDeleteSupplierBtn.addEventListener('click', () => DeleteSupplierModal.classList.remove('active'));
    }
}