// Funciones globales unificadas para apertura y cierre de modales
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

// Filtro de búsqueda en el modal de proveedores
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

// Flujo de modales en cadena (Paso 1 -> Paso 2)
function seleccionarProveedor(id, nombre) {
    document.getElementById('compra_id_proveedor').value = id;
    document.getElementById('compra_nombre_proveedor').value = nombre;
    
    cerrarModal('modalElegirProveedor');
    abrirModal('modalRegistrarCompra');
}

function regresarAPaso1() {
    cerrarModal('modalRegistrarCompra');
    abrirModal('modalElegirProveedor');
}

let productoIndex = 0;

// Configuración al cargar el documento (Restricciones e Integración de Inputs Opcionales)
document.addEventListener('DOMContentLoaded', () => {
    // Marcamos los inputs auxiliares de la compra como opcionales para el Validador Global
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
            el.classList.add('opcional'); // Esta clase hace que tu Form Global Validator lo ignore
            
            // Impide ingresar cero o valores negativos en tiempo real
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

// FORM GLOBAL VALIDATOR INTEGRADO (Sin mensajes de error visibles)
let errorTimeout = null; 
document.addEventListener('submit', (e) => {
    const currentForm = e.target;
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
        // Omite validación si tiene la clase opcional
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

    // Validación adicional: Comprobar que haya al menos un producto en la tabla de compras
    const tbodyDetalle = currentForm.querySelector('#tbodyDetalleNuevaCompra');
    if (tbodyDetalle) {
        const filasProductos = tbodyDetalle.querySelectorAll('.item-compra-row');
        if (filasProductos.length === 0) {
            isFormInvalid = true;
        }
    }

    if (isFormInvalid) {
        e.preventDefault();
        // Se resalta el borde pero no se muestra ningún texto descriptivo
        if (errorSummary) {
            errorSummary.textContent = "";
            errorSummary.classList.remove('active');

            errorTimeout = setTimeout(() => {
                formControls.forEach(c => c.classList.remove('input-error-border'));
            }, 4000); 
        }
    }
});

// Al seleccionar un producto, cargamos sus % de ganancia base
function alSeleccionarProducto() {
    const selector = document.getElementById('selector_producto_compra');
    const option = selector.options[selector.selectedIndex];

    if (option && option.value !== "") {
        const porcContado = parseFloat(option.getAttribute('data-porc-contado')) || "";
        const porcCredito = parseFloat(option.getAttribute('data-porc-credito')) || "";

        document.getElementById('input_porc_contado').value = porcContado > 0 ? porcContado : "";
        document.getElementById('input_porc_credito').value = porcCredito > 0 ? porcCredito : "";
    } else {
        document.getElementById('input_porc_contado').value = "";
        document.getElementById('input_porc_credito').value = "";
    }

    recalcularPreciosVentaModal();
}

// Recalcula en tiempo real los precios sugeridos en la vista previa
function recalcularPreciosVentaModal() {
    const costoUnitario = parseFloat(document.getElementById('input_costo_unitario').value) || 0;
    const porcContado = parseFloat(document.getElementById('input_porc_contado').value) || 0;
    const porcCredito = parseFloat(document.getElementById('input_porc_credito').value) || 0;

    if (costoUnitario > 0 && porcContado > 0 && porcCredito > 0) {
        const pContadoCalc = costoUnitario * (1 + (porcContado / 100));
        const pCreditoCalc = costoUnitario * (1 + (porcCredito / 100));

        document.getElementById('txt_precio_contado_calc').innerText = `${pContadoCalc.toFixed(2)}`;
        document.getElementById('txt_precio_credito_calc').innerText = `${pCreditoCalc.toFixed(2)}`;
    } else {
        document.getElementById('txt_precio_contado_calc').innerText = "0.00";
        document.getElementById('txt_precio_credito_calc').innerText = "0.00";
    }
}

// Agrega la fila a la tabla dinámicamente (alertas eliminadas)
function agregarProductoALaTabla(e) {
    if (e && e.preventDefault) e.preventDefault();

    const selector = document.getElementById('selector_producto_compra');
    const idProducto = selector.value;
    const optionSeleccionada = selector.options[selector.selectedIndex];
    const nombreProducto = optionSeleccionada ? optionSeleccionada.getAttribute('data-nombre') : '';
    
    const cantVal = document.getElementById('input_cantidad_compra').value.trim();
    const costoVal = document.getElementById('input_costo_unitario').value.trim();
    const contadoVal = document.getElementById('input_porc_contado').value.trim();
    const creditoVal = document.getElementById('input_porc_credito').value.trim();

    // Validaciones específicas del botón "Agregar" sin mensajes emergentes
    if (!idProducto) return;
    if (cantVal === "" || costoVal === "" || contadoVal === "" || creditoVal === "") return;

    const cantidad = parseInt(cantVal, 10);
    const costoUnitario = parseFloat(costoVal);
    const porcContado = parseFloat(contadoVal);
    const porcCredito = parseFloat(creditoVal);

    if (isNaN(cantidad) || cantidad <= 0 || isNaN(costoUnitario) || costoUnitario <= 0 || isNaN(porcContado) || porcContado <= 0 || isNaN(porcCredito) || porcCredito <= 0) {
        return;
    }

    // Quitar fila vacía
    const rowVacia = document.getElementById('row_vacia_tabla');
    if (rowVacia) rowVacia.remove();

    const subtotal = cantidad * costoUnitario;
    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    
    const nuevaFila = document.createElement('tr');
    nuevaFila.className = 'item-compra-row';
    
    nuevaFila.innerHTML = `
        <td class="detail-product-name">
            <input type="hidden" name="productos[${productoIndex}][id_producto]" value="${idProducto}">
            ${nombreProducto}
        </td>
        <td>
            <input type="hidden" name="productos[${productoIndex}][cantidad]" value="${cantidad}">
            ${cantidad}
        </td>
        <td>
            <input type="hidden" name="productos[${productoIndex}][costo_unitario]" value="${costoUnitario.toFixed(2)}">
            ${costoUnitario.toFixed(2)}
        </td>
        <td>
            <input type="hidden" name="productos[${productoIndex}][porc_contado]" value="${porcContado}">
            ${porcContado}%
        </td>
        <td>
            <input type="hidden" name="productos[${productoIndex}][porc_credito]" value="${porcCredito}">
            ${porcCredito}%
        </td>
        <td class="row-subtotal" data-valor="${subtotal}">${subtotal.toFixed(2)}</td>
        <td>
            <button type="button" class="action-btn delete-btn" onclick="eliminarFilaProducto(this)">
                <span class="material-symbols-outlined">delete</span>Eliminar
            </button>
        </td>
    `;
    
    tbody.appendChild(nuevaFila);
    productoIndex++;
    
    // Limpiar inputs
    selector.value = "";
    document.getElementById('input_cantidad_compra').value = 1;
    document.getElementById('input_costo_unitario').value = "";
    document.getElementById('input_porc_contado').value = "";
    document.getElementById('input_porc_credito').value = "";
    recalcularPreciosVentaModal();
    
    calcularGranTotalCompra();
}

function eliminarFilaProducto(btn) {
    btn.closest('tr').remove();
    
    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    if (tbody.children.length === 0) {
        tbody.innerHTML = `
            <tr id="row_vacia_tabla">
                <td colspan="7" class="text-muted" style="text-align: center !important; padding: 20px;">
                    Ningún producto agregado a esta compra todavía.
                </td>
            </tr>
        `;
    }
    calcularGranTotalCompra();
}

function calcularGranTotalCompra() {
    let granTotal = 0;
    const subtotales = document.querySelectorAll('#tbodyDetalleNuevaCompra .row-subtotal');
    
    subtotales.forEach(celda => {
        granTotal += parseFloat(celda.getAttribute('data-valor')) || 0;
    });
    
    document.getElementById('txt_monto_total_compra').innerText = `${granTotal.toFixed(2)}`;
    document.getElementById('input_monto_total_hidden').value = granTotal.toFixed(2);
}