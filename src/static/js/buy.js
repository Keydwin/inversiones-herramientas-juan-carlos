
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
            errorSummary.textContent = "";
            errorSummary.classList.remove('active');

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
    const costo = parseFloat(document.getElementById('input_costo_unitario').value) || 0;
    const porcContado = parseFloat(document.getElementById('input_porc_contado').value) || 0;
    const porcCredito = parseFloat(document.getElementById('input_porc_credito').value) || 0;

    const precioContado = costo + (costo * (porcContado / 100));
    const precioCredito = costo + (costo * (porcCredito / 100));

    document.getElementById('txt_precio_contado_calc').innerText = precioContado.toFixed(2);
    document.getElementById('txt_precio_credito_calc').innerText = precioCredito.toFixed(2);
}


function agregarProductoALaTabla() {
    const select = document.getElementById('selector_producto_compra');
    const idProducto = select.value;
    
    if (!idProducto) {
        alert('Por favor seleccione un producto.');
        return;
    }

    const option = select.options[select.selectedIndex];
    const nombreProducto = option.getAttribute('data-nombre') || option.text;
    const cantidad = parseInt(document.getElementById('input_cantidad_compra').value) || 0;
    const costoUnitario = parseFloat(document.getElementById('input_costo_unitario').value) || 0;

    if (cantidad <= 0 || costoUnitario <= 0) {
        alert('Por favor ingrese una cantidad y costo unitario válidos.');
        return;
    }


    const precioContado = parseFloat(document.getElementById('txt_precio_contado_calc').innerText) || 0;
    const precioCredito = parseFloat(document.getElementById('txt_precio_credito_calc').innerText) || 0;
    const subtotal = cantidad * costoUnitario;

    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    

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
            ${precioContado.toFixed(2)}
            <input type="hidden" name="productos[${index}][PrecioDecontado]" value="${precioContado.toFixed(2)}">
        </td>
        <td>
            ${precioCredito.toFixed(2)}
            <input type="hidden" name="productos[${index}][PrecioCredito]" value="${precioCredito.toFixed(2)}">
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
    const filas = tbody.querySelectorAll('.item-compra-row');

    filas.forEach((row, newIndex) => {
        row.querySelectorAll('input[type="hidden"]').forEach(input => {
            input.name = input.name.replace(/productos\[\d+\]/, `productos[${newIndex}]`);
        });
    });
}

function eliminarFila(btn) {
    const row = btn.closest('tr');
    row.remove();
    
    const tbody = document.getElementById('tbodyDetalleNuevaCompra');
    const filasRestantes = tbody.querySelectorAll('.item-compra-row');
    
    if (filasRestantes.length === 0) {
        tbody.innerHTML = `
            <tr id="row_vacia_tabla">
                <td colspan="7" class="text-center">No se han agregado productos a la lista de compra</td>
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

    document.getElementById('txt_monto_total_compra').innerText = total.toFixed(2);
    document.getElementById('input_monto_total_hidden').value = total.toFixed(2);
}


function limpiarEntradasModal() {
    document.getElementById('selector_producto_compra').value = '';
    document.getElementById('input_cantidad_compra').value = '';
    document.getElementById('input_costo_unitario').value = '';
    document.getElementById('input_porc_contado').value = '';
    document.getElementById('input_porc_credito').value = '';
    document.getElementById('txt_precio_contado_calc').innerText = '0.00';
    document.getElementById('txt_precio_credito_calc').innerText = '0.00';
}