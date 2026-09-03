// Global variable to store total sale amount
let totalVenta = 0.0;

//  Triggered when selecting a product from the dropdown
function alSeleccionarProductoVenta() {
    const selectorProducto = document.getElementById('selector_producto_venta');
    if (!selectorProducto) return;
    
    const optionSeleccionada = selectorProducto.options[selectorProducto.selectedIndex];
    
    if (!selectorProducto.value) {
        document.getElementById('input_precio_unitario').value = '';
        return;
    }

    // Read current payment type
    const tipoPago = document.getElementById('selector_tipo_pago').value;
    
    // Get prices from option data attributes
    const precioContado = parseFloat(optionSeleccionada.getAttribute('data-precio-contado')) || 0;
    const precioCredito = parseFloat(optionSeleccionada.getAttribute('data-precio-credito')) || 0;

    // Set price based on selected payment type
    const precioAplicado = (tipoPago === 'Crédito') ? precioCredito : precioContado;
    document.getElementById('input_precio_unitario').value = precioAplicado.toFixed(2);
}

//  Triggered when changing payment type (Cash / Credit)
function alCambiarTipoPago() {
    // Update price for currently selected product
    alSeleccionarProductoVenta();
}

//  Add row to the sales table
function agregarProductoVentaTabla() {
    const selectorProducto = document.getElementById('selector_producto_venta');
    const selectorTipoPago = document.getElementById('selector_tipo_pago');
    const inputCantidad = document.getElementById('input_cantidad_venta');
    const inputPrecio = document.getElementById('input_precio_unitario');
    const tbody = document.getElementById('tbodyDetalleNuevaVenta');
    const rowVacia = document.getElementById('row_vacia_tabla');

    const idProducto = selectorProducto.value;
    const nombreProducto = selectorProducto.options[selectorProducto.selectedIndex]?.getAttribute('data-nombre');
    const cantidad = parseInt(inputCantidad.value);
    const precioUnitario = parseFloat(inputPrecio.value);

    // Silent validation: stop if data is missing or invalid
    if (!idProducto || isNaN(cantidad) || cantidad <= 0 || isNaN(precioUnitario)) {
        return;
    }

    const subtotal = cantidad * precioUnitario;

    // Remove empty table placeholder row if present
    if (rowVacia) {
        rowVacia.remove();
    }

    const tr = document.createElement('tr');
    tr.setAttribute('data-subtotal', subtotal);
    tr.innerHTML = `
        <td>
            ${nombreProducto}
            <input type="hidden" name="id_producto[]" value="${idProducto}">
        </td>
        <td>
            ${cantidad}
            <input type="hidden" name="cantidad[]" value="${cantidad}">
        </td>
        <td>${precioUnitario.toFixed(2)}</td>
        <td class="col-subtotal">${subtotal.toFixed(2)}</td>
        <td>
            <button type="button" class="action-btn delete-btn" onclick="eliminarFila(this)">
                <span class="material-symbols-outlined">delete</span>Eliminar
            </button>
        </td>
    `;

    tbody.appendChild(tr);

    // Disable payment type select after adding the first item
    if (selectorTipoPago) {
        selectorTipoPago.disabled = true;
    }

    // Recalculate total
    recalcularTotalVenta();

    // Reset input fields
    selectorProducto.value = '';
    inputCantidad.value = '';
    inputPrecio.value = '';
}

//  Remove a row from the table
function eliminarFila(btn) {
    const tr = btn.closest('tr');
    tr.remove();

    const tbody = document.getElementById('tbodyDetalleNuevaVenta');
    const selectorTipoPago = document.getElementById('selector_tipo_pago');

    // Restore empty state and enable payment type if table is empty
    if (tbody.children.length === 0) {
        tbody.innerHTML = `
            <tr id="row_vacia_tabla">
                <td colspan="5" class="text-center">No se han agregado productos a la lista de venta</td>
            </tr>
        `;
        if (selectorTipoPago) {
            selectorTipoPago.disabled = false;
        }
    }

    recalcularTotalVenta();
}

// Alias for backwards compatibility
function eliminarFilaVenta(btn) {
    eliminarFila(btn);
}

//  Recalculate grand total amount
function recalcularTotalVenta() {
    const filas = document.querySelectorAll('#tbodyDetalleNuevaVenta tr[data-subtotal]');
    let total = 0;

    filas.forEach(fila => {
        total += parseFloat(fila.getAttribute('data-subtotal')) || 0;
    });

    const elemText = document.getElementById('txt_monto_total_venta');
    const elemInput = document.getElementById('input_monto_total_hidden');

    if (elemText) elemText.textContent = total.toFixed(2);
    if (elemInput) elemInput.value = total.toFixed(2);
}

//  Base Helper Functions for Modals 
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

//  Sale Detail Modals 
function abrirModalDetalle(idVenta) {
    abrirModal(`modalDetalle${idVenta}`);
}

function cerrarModalDetalle(idVenta) {
    cerrarModal(`modalDetalle${idVenta}`);
}

//  General Report Modal 
function abrirModalReporte() {
    abrirModal('modalReportePdf');
}

function cerrarModalReporte() {
    cerrarModal('modalReportePdf');
}

//  Seller Personal Report Modal 
function abrirModalReporteVendedor() {
    abrirModal('modalReporteVendedorPdf');
}

function cerrarModalReporteVendedor() {
    cerrarModal('modalReporteVendedorPdf');
}

// Re-enable payment type select before submitting form to Flask
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formRegistroVenta');
    if (form) {
        form.addEventListener('submit', () => {
            const selectorTipoPago = document.getElementById('selector_tipo_pago');
            if (selectorTipoPago) {
                selectorTipoPago.disabled = false;
            }
        });
    }
});