document.addEventListener('DOMContentLoaded', () => {
// CONTROL SEGURO DE LA MODAL DE PRODUCTOS
    const productModal = document.getElementById('ProductModal');
    const openProductBtn = document.getElementById('openProductBtn');
    const closeProductBtn = document.getElementById('closeProductBtn');

    if (openProductBtn && productModal && closeProductBtn) {
        openProductBtn.addEventListener('click', () => {
            const form = productModal.querySelector('form');
            if (form) form.reset();
            productModal.classList.add('active');
        });

        closeProductBtn.addEventListener('click', () => {
            productModal.classList.remove('active');
        });
    }

    const form = document.getElementById('Codigo')?.closest('form');
    if (form) {
        form.setAttribute('autocomplete', 'off');
    }

    // Code input
    const inputCodigo = document.getElementById('Codigo');
    if (inputCodigo) {
        inputCodigo.maxLength = 10;
        inputCodigo.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Product Name input 
    const inputNombre = document.getElementById('NombreProducto');
    if (inputNombre) {
        inputNombre.maxLength = 30;
        inputNombre.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 ]/g, '');
        });
    }

    // Description input 
    const inputDescripcion = document.getElementById('Descripcion');
    if (inputDescripcion) {
        inputDescripcion.maxLength = 40;
        inputDescripcion.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 .,()-]/g, '');
        });
    }

    // Brand ID input 
    const inputIdMarca = document.getElementById('IdMarca');
    if (inputIdMarca) {
        inputIdMarca.maxLength = 10;
        inputIdMarca.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Cash Percentage input 
    const inputPorcentajeContado = document.getElementById('PorcenajeDeContado');
    if (inputPorcentajeContado) {
        inputPorcentajeContado.maxLength = 3;
        inputPorcentajeContado.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Credit Percentage input 
    const inputPorcentajeCredito = document.getElementById('PorcentajeCredito');
    if (inputPorcentajeCredito) {
        inputPorcentajeCredito.maxLength = 3;
        inputPorcentajeCredito.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Cash Price input 
    const inputPrecioContado = document.getElementById('PrecioDeContado');
    if (inputPrecioContado) {
        inputPrecioContado.maxLength = 10;
        inputPrecioContado.addEventListener('input', (e) => {
            let value = e.target.value.replace(/[^0-9.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    }

    // Credit Price input 
    const inputPrecioCredito = document.getElementById('PrecioCredito');
    if (inputPrecioCredito) {
        inputPrecioCredito.maxLength = 10;
        inputPrecioCredito.addEventListener('input', (e) => {
            let value = e.target.value.replace(/[^0-9.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    }



    const editModal = document.getElementById('EditProductModal');
    const closeEditProductBtn = document.getElementById('closeEditProductBtn');

    if (closeEditProductBtn && editModal) {
        closeEditProductBtn.addEventListener('click', () => {

            editModal.classList.remove('active');
            editModal.style.display = 'none';
        });
    }


    // Disable autocomplete on the Edit Form
    const editForm = document.getElementById('EditProductForm');
    if (editForm) editForm.setAttribute('autocomplete', 'off');

    // Code input
    const editCodigo = document.getElementById('CodigoEdicion');
    if (editCodigo) {
        editCodigo.maxLength = 10;
        editCodigo.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Product Name input 
    const editNombre = document.getElementById('NombreProductoEdicion');
    if (editNombre) {
        editNombre.maxLength = 50;
        editNombre.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 ]/g, '');
        });
    }

    // Description input 
    const editDescripcion = document.getElementById('DescripcionEdicion');
    if (editDescripcion) {
        editDescripcion.maxLength = 40;
        editDescripcion.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 .,()-]/g, '');
        });
    }

    // Brand ID input 
    const editIdMarca = document.getElementById('IdMarcaEdicion');
    if (editIdMarca) {
        editIdMarca.maxLength = 10;
        editIdMarca.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Cash Percentage input 
    const editPorcentajeContado = document.getElementById('PorcenajeDeContadoEdicion');
    if (editPorcentajeContado) {
        editPorcentajeContado.maxLength = 3;
        editPorcentajeContado.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Credit Percentage input 
    const editPorcentajeCredito = document.getElementById('PorcentajeCreditoEdicion');
    if (editPorcentajeCredito) {
        editPorcentajeCredito.maxLength = 3;
        editPorcentajeCredito.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Cash Price input 
    const editPrecioContado = document.getElementById('PrecioDeContadoEdicion');
    if (editPrecioContado) {
        editPrecioContado.maxLength = 10;
        editPrecioContado.addEventListener('input', (e) => {
            let value = e.target.value.replace(/[^0-9.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    }

    const editPrecioCredito = document.getElementById('PrecioCreditoEdicion');
    if (editPrecioCredito) {
        editPrecioCredito.maxLength = 10;
        editPrecioCredito.addEventListener('input', (e) => {
            let value = e.target.value.replace(/[^0-9.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    }


    const deleteModal = document.getElementById('DeleteProductModal');
    const closeDeleteBtn = document.getElementById('closeDeleteProductBtn');

    if (closeDeleteBtn && deleteModal) {
        closeDeleteBtn.addEventListener('click', () => {

            deleteModal.classList.remove('active'); 
        });
    }
})

function OpenProductUpdateModal(id, codigo, nombre, descripcion, idMarca, pctContado, precioContado, pctCredito, precioCredito) {
    const editForm = document.getElementById('EditProductForm');
    const editModal = document.getElementById('EditProductModal');

    if (editForm) {
        editForm.action = `/productos/modificar/${id}`;
    }

    if (document.getElementById('CodigoEdicion')) document.getElementById('CodigoEdicion').value = codigo;
    if (document.getElementById('NombreProductoEdicion')) document.getElementById('NombreProductoEdicion').value = nombre;
    if (document.getElementById('DescripcionEdicion')) document.getElementById('DescripcionEdicion').value = descripcion;
    if (document.getElementById('IdMarcaEdicion')) document.getElementById('IdMarcaEdicion').value = idMarca;
    if (document.getElementById('PorcenajeDeContadoEdicion')) document.getElementById('PorcenajeDeContadoEdicion').value = pctContado;
    if (document.getElementById('PrecioDeContadoEdicion')) document.getElementById('PrecioDeContadoEdicion').value = precioContado;
    if (document.getElementById('PorcentajeCreditoEdicion')) document.getElementById('PorcentajeCreditoEdicion').value = pctCredito;
    if (document.getElementById('PrecioCreditoEdicion')) document.getElementById('PrecioCreditoEdicion').value = precioCredito;

    if (editModal) {
        editModal.classList.add('active');
        editModal.style.display = 'flex';
    }

}



function OpenProductDeleteModal(id, nombre) {
    const deleteForm = document.getElementById('DeleteProductForm');
    const deleteModal = document.getElementById('DeleteProductModal');

    if (deleteForm) {
        deleteForm.action = `/productos/eliminar/${id}`;
    }

    if (deleteModal) {
        deleteModal.classList.add('active');
    }
}