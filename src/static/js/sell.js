// Variable global para almacenar el total de la venta
let totalVenta = 0.0;

// 1. Evento al seleccionar un producto en el <select>
function alSeleccionarProductoVenta() {
    const selectorProducto = document.getElementById('selector_producto_venta');
    if (!selectorProducto) return;
    
    const optionSeleccionada = selectorProducto.options[selectorProducto.selectedIndex];
    
    if (!selectorProducto.value) {
        document.getElementById('input_precio_unitario').value = '';
        return;
    }

    // Leer tipo de pago actual
    const tipoPago = document.getElementById('selector_tipo_pago').value;
    
    // Obtener precios desde los data-attributes del <option>
    const precioContado = parseFloat(optionSeleccionada.getAttribute('data-precio-contado')) || 0;
    const precioCredito = parseFloat(optionSeleccionada.getAttribute('data-precio-credito')) || 0;

    // Asignar precio al input visual según tipo de pago
    const precioAplicado = (tipoPago === 'Crédito') ? precioCredito : precioContado;
    document.getElementById('input_precio_unitario').value = precioAplicado.toFixed(2);
}

// 2. Evento al cambiar el tipo de pago (Contado / Crédito)
function alCambiarTipoPago() {
    // Actualiza el precio del producto que esté actualmente seleccionado en el combo
    alSeleccionarProductoVenta();
}

// 3. Agregar fila a la tabla visual
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

    // Validación silenciosa: si faltan datos o son inválidos, se detiene sin mostrar alerta
    if (!idProducto || isNaN(cantidad) || cantidad <= 0 || isNaN(precioUnitario)) {
        return;
    }

    const subtotal = cantidad * precioUnitario;

    // Eliminar la fila "No se han agregado productos" si existe
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

    // Bloquear el select de tipo de pago al agregar el primer producto
    if (selectorTipoPago) {
        selectorTipoPago.disabled = true;
    }

    // Recalcular total visual
    recalcularTotalVenta();

    // Resetear controles
    selectorProducto.value = '';
    inputCantidad.value = '';
    inputPrecio.value = '';
}

// 4. Eliminar fila de la tabla
function eliminarFila(btn) {
    const tr = btn.closest('tr');
    tr.remove();

    const tbody = document.getElementById('tbodyDetalleNuevaVenta');
    const selectorTipoPago = document.getElementById('selector_tipo_pago');

    // Si la tabla queda vacía, restaurar estado inicial y desbloquear el tipo de pago
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

// Alias por compatibilidad
function eliminarFilaVenta(btn) {
    eliminarFila(btn);
}

// 5. Recalcular total general de la venta (Visual)
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

// --- Funciones Base Generales para Modales ---
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

// --- Modales de Detalle de Venta ---
function abrirModalDetalle(idVenta) {
    abrirModal(`modalDetalle${idVenta}`);
}

function cerrarModalDetalle(idVenta) {
    cerrarModal(`modalDetalle${idVenta}`);
}

// --- Modal Reporte General ---
function abrirModalReporte() {
    abrirModal('modalReportePdf');
}

function cerrarModalReporte() {
    cerrarModal('modalReportePdf');
}

// --- Modal Mi Reporte (Vendedor Personal) ---
function abrirModalReporteVendedor() {
    abrirModal('modalReporteVendedorPdf');
}

function cerrarModalReporteVendedor() {
    cerrarModal('modalReporteVendedorPdf');
}

// Habilitar el tipo de pago antes de enviar el formulario POST a Flask
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