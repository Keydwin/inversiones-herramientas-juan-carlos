function abrirModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('active');
    }
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('active');
    }
}

function abrirModalDetalle(idCompra) {
    abrirModal(`modalDetalle${idCompra}`);
}

function cerrarModalDetalle(idCompra) {
    cerrarModal(`modalDetalle${idCompra}`);
}

function abrirModalReporte() {
    abrirModal('modalReportePdf');
}

function cerrarModalReporte() {
    cerrarModal('modalReportePdf');
}

function filtrarProveedoresModal() {
    let input = document.getElementById('buscarProveedorModal').value.toLowerCase();
    let rows = document.querySelectorAll('#tbodyProveedoresModal .provider-row-select');
    
    rows.forEach(row => {
        let nombreCell = row.querySelector('.provider-name-cell');
        let nombre = nombreCell ? nombreCell.getAttribute('data-name').toLowerCase() : '';
        if (nombre.includes(input)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function seleccionarProveedor(id, nombre) {
    const elId = document.getElementById('compra_id_proveedor');
    const elNombre = document.getElementById('compra_nombre_proveedor');
    if (elId) elId.value = id;
    if (elNombre) elNombre.value = nombre;
    
    cerrarModal('modalElegirProveedor');
    abrirModal('modalRegistrarCompra');
}

function regresarAPaso1() {
    cerrarModal('modalRegistrarCompra');
    abrirModal('modalElegirProveedor');
}

let productoIndex = 0;

document.addEventListener('DOMContentLoaded', () => {
    const inputsAuxiliares = [
        'selector_producto_compra',
        'input_cantidad_compra',
        'input_costo_unitario',
        'input_porc_contado',
        'input_porc_credito'
    ];

    inputsAuxiliares.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.add('opcional'); 

            if (id !== 'selector_producto_compra') {
                el.setAttribute('min', id === 'input_cantidad_compra' ? '1' : '0.01');
                el.addEventListener('input', function () {
                    const val = parseFloat(this.value);
                    if (this.value !== "" && (isNaN(val) || val <= 0)) {
                        this.value = "";
                    }
                    recalcularPreciosVentaModal();
                });
            }
        }
    });
});

let errorTimeout = null; 
document.addEventListener('submit', (e) => {
    const currentForm = e.target;
    
    if (currentForm.method.toUpperCase() === 'GET') {
        return;
    }

    const formControls = currentForm.querySelectorAll(
        'input[type="text"], input[type="number"], input:not([type]), textarea, select'
    );
    
    let isFormInvalid = false;
    const errorSummary = currentForm.querySelector('.form-error');

    if (errorSummary) {
        errorSummary.textContent = "";
        errorSummary.classList.remove('active');
    }
    if (errorTimeout) clearTimeout(errorTimeout);

    formControls.forEach(control => {
        if (control.classList.contains('opcional')) {
            control.value = control.value.trim();
            return;
        }

        control.classList.remove('input-error-border');

        if (control.tagName.toLowerCase() === 'select') {
            if (control.value === '' || control.value === '0') {
                isFormInvalid = true;
                control.classList.add('input-error-border');
            }
        } else if (control.type === 'number') {
            if (control.value === '' || parseFloat(control.value) < 0) {
                isFormInvalid = true;
                control.classList.add('input-error-border');
            }
        } else {
            const cleanValue = control.value.trim();
            if (cleanValue === '') {
                isFormInvalid = true;
                control.value = ''; 
                control.classList.add('input-error-border');
            } else {
                control.value = cleanValue; 
            }
        }
    });

    const tbodyDetalle = currentForm.querySelector('#tbodyDetalleNuevaCompra');
    if (tbodyDetalle) {
        const filasProductos = tbodyDetalle.querySelectorAll('.item-compra-row');
        if (filasProductos.length === 0) {
            isFormInvalid = true;
        }
    }

    if (isFormInvalid) {
        e.preventDefault();

        if (errorSummary) {
            errorTimeout = setTimeout(() => {
                formControls.forEach(c => c.classList.remove('input-error-border'));
            }, 4000); 
        }
    }
});

function alSeleccionarProducto() {
    const select = document.getElementById('selector_producto_compra');
    if (!select || select.selectedIndex === -1) return;

    const option = select.options[select.selectedIndex];
    
    if (option && option.value) {
        const porcContado = option.getAttribute('data-porc-contado') || 0;
        const porcCredito = option.getAttribute('data-porc-credito') || 0;

        document.getElementById('input_porc_contado').value = porcContado;
        document.getElementById('input_porc_credito').value = porcCredito;
    } else {
        document.getElementById('input_porc_contado').value = '';
        document.getElementById('input_porc_credito').value = '';
    }
    
    recalcularPreciosVentaModal();
}

function recalcularPreciosVentaModal() {
    const costoEl = document.getElementById('input_costo_unitario');
    const porcContadoEl = document.getElementById('input_porc_contado');
    const porcCreditoEl = document.getElementById('input_porc_credito');
    
    if (!costoEl || !porcContadoEl || !porcCreditoEl) return;

    const costo = parseFloat(costoEl.value) || 0;
    const porcContado = parseFloat(porcContadoEl.value) || 0;
    const porcCredito = parseFloat(porcCreditoEl.value) || 0;

    const precioContado = costo + (costo * (porcContado / 100));
    const precioCredito = costo + (costo * (porcCredito / 100));

    const txtContado = document.getElementById('txt_precio_contado_calc');
    const txtCredito = document.getElementById('txt_precio_credito_calc');
    if (txtContado) txtContado.innerText = precioContado.toFixed(2);
    if (txtCredito) txtCredito.innerText = precioCredito.toFixed(2);
}

function agregarProductoALaTabla() {
    const select = document.getElementById('selector_producto_compra');
    if (!select) return;

    const idProducto = select.value;
    
    if (!idProducto) {
        return;
    }

    const option = select.options[select.selectedIndex];
    const nombreProducto = option.getAttribute('data-nombre') || option.text;
    const cantidad = parseInt(document.getElementById('input_cantidad_compra').value) || 0;
    const costoUnitario = parseFloat(document.getElementById('input_costo_unitario').value) || 0;

    if (cantidad <= 0 || costoUnitario <= 0) {
        return;
    }

    const precioContado = parseFloat(document.getElementById('txt_precio_contado_calc').innerText) || 0;
    const precioCredito = parseFloat(document.getElementById('txt_precio_credito_calc').innerText) || 0;
    const subtotal = cantidad * costoUnitario;

    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    if (!tbody) return;

    const rowVacia = document.getElementById('row_vacia_tabla');
    if (rowVacia) {
        rowVacia.remove();
    }

    const index = tbody.querySelectorAll('.item-compra-row').length;

    const row = document.createElement('tr');
    row.classList.add('item-compra-row'); 
    row.innerHTML = `
        <td>
            ${nombreProducto}
            <input type="hidden" name="productos[${index}][IdProducto]" value="${idProducto}">
        </td>
        <td>
            ${cantidad}
            <input type="hidden" name="productos[${index}][Cantidad]" value="${cantidad}">
        </td>
        <td>
            ${costoUnitario.toFixed(2)}
            <input type="hidden" name="productos[${index}][CostoUnitario]" value="${costoUnitario.toFixed(2)}">
        </td>
        <td>
            ${subtotal.toFixed(2)}
            <input type="hidden" name="productos[${index}][Subtotal]" value="${subtotal.toFixed(2)}">
        </td>
        <td>
            <button type="button" class="action-btn delete-btn" onclick="eliminarFila(this)">
                <span class="material-symbols-outlined">delete</span>Eliminar
            </button>
        </td>
    `;

    tbody.appendChild(row);
    actualizarTotalGeneral();
    limpiarEntradasModal();
}

function reindexarFilas() {
    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    if (!tbody) return;
    const filas = tbody.querySelectorAll('.item-compra-row');

    filas.forEach((row, newIndex) => {
        row.querySelectorAll('input[type="hidden"]').forEach(input => {
            input.name = input.name.replace(/productos\[\d+\]/, `productos[${newIndex}]`);
        });
    });
}

function eliminarFila(btn) {
    const row = btn.closest('tr');
    if (row) row.remove();
    
    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    if (!tbody) return;
    const filasRestantes = tbody.querySelectorAll('.item-compra-row');
    
    if (filasRestantes.length === 0) {
        tbody.innerHTML = `
            <tr id="row_vacia_tabla">
                <td colspan="5" class="text-center">No se han agregado productos a la lista de compra</td>
            </tr>
        `;
    } else {
        reindexarFilas();
    }
    actualizarTotalGeneral();
}

function actualizarTotalGeneral() {
    let total = 0;
    const subtotales = document.querySelectorAll('input[name*="[Subtotal]"]');
    subtotales.forEach(input => {
        total += parseFloat(input.value) || 0;
    });

    const txtTotal = document.getElementById('txt_monto_total_compra');
    const inputTotal = document.getElementById('input_monto_total_hidden');
    if (txtTotal) txtTotal.innerText = total.toFixed(2);
    if (inputTotal) inputTotal.value = total.toFixed(2);
}

function limpiarEntradasModal() {
    const selector = document.getElementById('selector_producto_compra');
    const cant = document.getElementById('input_cantidad_compra');
    const costo = document.getElementById('input_costo_unitario');
    const pContado = document.getElementById('input_porc_contado');
    const pCredito = document.getElementById('input_porc_credito');
    const txtContado = document.getElementById('txt_precio_contado_calc');
    const txtCredito = document.getElementById('txt_precio_credito_calc');

    if (selector) selector.value = '';
    if (cant) cant.value = '';
    if (costo) costo.value = '';
    if (pContado) pContado.value = '';
    if (pCredito) pCredito.value = '';
    if (txtContado) txtContado.innerText = '0.00';
    if (txtCredito) txtCredito.innerText = '0.00';
}