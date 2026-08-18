document.addEventListener('DOMContentLoaded', () => {
    // 1. Vincular el botón Registrar de la interfaz con el modal de Proveedores
    const openSupplierModalBtn = document.getElementById('openSupplierModalBtn');
    const SupplierModal = document.getElementById('SupplierModal');
    const closeSupplierBtn = document.getElementById('closeSupplierBtn');
    
    if (openSupplierModalBtn && SupplierModal && closeSupplierBtn) {
        openSupplierModalBtn.addEventListener('click', () => {
            const form = SupplierModal.querySelector('form');
            if (form) form.reset();
            SupplierModal.classList.add('active');
        });
        closeSupplierBtn.addEventListener('click', () => SupplierModal.classList.remove('active'));
    }

    // Validación opcional para el campo de nombre del proveedor (solo letras y espacios)
    const supplierInput = document.getElementById('NombreProveedor');
    const updateSupplierInput = document.getElementById('UpdateNombreProveedor');

    if (supplierInput) {
        supplierInput.maxLength = 50;
        supplierInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    if (updateSupplierInput) {
        updateSupplierInput.maxLength = 50;
        updateSupplierInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }
});

// 2. Funciones globales para las acciones de la tabla (Modificar y Eliminar)
function openUpdateSupplierModal(id, nombre) {
    const UpdateSupplierModal = document.getElementById('UpdateSupplierModal');
    const UpdateSupplierForm = document.getElementById('UpdateSupplierForm');
    const closeUpdateSupplierBtn = document.getElementById('closeUpdateSupplierBtn');
    const UpdateNombreProveedor = document.getElementById('UpdateNombreProveedor');
    
    if (UpdateSupplierModal && UpdateSupplierForm && UpdateNombreProveedor && closeUpdateSupplierBtn) {
        UpdateSupplierForm.action = `/proveedores/modificar/${id}`;
        UpdateNombreProveedor.value = nombre;
        UpdateSupplierModal.classList.add('active');
        
        closeUpdateSupplierBtn.onclick = () => {
            UpdateSupplierModal.classList.remove('active');
        };
    }
}

function openDeleteSupplierModal(id) {
    const DeleteSupplierModal = document.getElementById('DeleteSupplierModal');
    const DeleteSupplierForm = document.getElementById('DeleteSupplierForm');
    const closeDeleteSupplierBtn = document.getElementById('closeDeleteSupplierBtn');
    
    if (DeleteSupplierModal && DeleteSupplierForm && closeDeleteSupplierBtn) {
        DeleteSupplierForm.action = `/proveedores/delete/${id}`;
        DeleteSupplierModal.classList.add('active');   
        
        closeDeleteSupplierBtn.onclick = () => {
            DeleteSupplierModal.classList.remove('active');
        };
    }
}