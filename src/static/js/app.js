document.addEventListener('DOMContentLoaded', () => {
            
    // MENU & SIDEBAR CONTROL
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const dropdowns = document.querySelectorAll('.dropdown-toggle');

    dropdowns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const submenu = btn.nextElementSibling;
            document.querySelectorAll('.submenu').forEach(sub => {
                if (sub !== submenu) {
                    sub.classList.remove('show');
                    sub.previousElementSibling.classList.remove('dropdown-open');
                }
            });
            if (submenu) {
                submenu.classList.toggle('show');
                btn.classList.toggle('dropdown-open');
            }
        });
    });

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
    }

    // FORM GLOBAL VALIDATOR 
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

            // Permitir omitir la marca en el registro de productos
            if (control.tagName.toLowerCase() === 'select') {
                if (control.value === '' || control.value === '0') {
                    isFormInvalid = true;
                    control.classList.add('input-error-border');
                }
            }
            if (control.type === 'number') {
                if (control.value === '' || parseFloat(control.value) < 0) {
                    isFormInvalid = true;
                    control.classList.add('input-error-border');
                }
            } 
            else if (control.tagName.toLowerCase() !== 'select') {
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

        if (isFormInvalid) {
            e.preventDefault();
            if (errorSummary) {
                errorSummary.textContent = "Por favor ingrese todos los datos solicitados";
                errorSummary.classList.add('active');

                errorTimeout = setTimeout(() => {
                    errorSummary.classList.remove('active');
                    setTimeout(() => {
                        if (!errorSummary.classList.contains('active')) {
                            errorSummary.textContent = ""; 
                        }
                    }, 250);
                    formControls.forEach(c => c.classList.remove('input-error-border'));
                }, 4000); 
            }
        }
    });

    // LIVE INPUT CLEANUP
    document.addEventListener('input', (e) => {
        const control = e.target;
        control.classList.remove('input-error-border');
        const currentForm = control.closest('form');
        if (currentForm) {
            const errorSummary = currentForm.querySelector('.form-error');
            if (errorSummary) errorSummary.classList.remove('active');
        }
    });
    
    document.addEventListener('click', (e) => {
        const cancelBtn = e.target.closest('.btn-cancel');
        if (cancelBtn) {
            const modal = cancelBtn.closest('.modal-overlay');
            if (modal) {
                const form = modal.querySelector('form');
                if (form) {
                    const errorSummary = form.querySelector('.form-error');
                    if (errorSummary) {
                        errorSummary.textContent = "";
                        errorSummary.classList.remove('active');
                    }
                    form.querySelectorAll('input, textarea, select').forEach(input => {
                        input.classList.remove('input-error-border');
                    });
                }
            }
        }
    });

    // FLASH MESSAGES TIMEOUT
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500); 
        }, 2000);
    });

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
        inputDescripcion.maxLength = 50;
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


    const openTrademarkModalBtn = document.getElementById('openTrademarkModalBtn');
    const TrademarkModal = document.getElementById('TrademarkModal');
    const closeTrademarkBtn = document.getElementById('closeTrademarkBtn');
    const trademarkInput = document.getElementById('Marca');
    const UpdateTrademark = document.getElementById('UpdateTrademark');

    if (openTrademarkModalBtn && TrademarkModal && closeTrademarkBtn) {
        openTrademarkModalBtn.addEventListener('click', () => {
            const form = TrademarkModal.querySelector('form');
            if (form) form.reset();
            TrademarkModal.classList.add('active');
        });
        closeTrademarkBtn.addEventListener('click', () => TrademarkModal.classList.remove('active'));
    }

    if (trademarkInput) {
        trademarkInput.maxLength = 25;
        trademarkInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    if (UpdateTrademark) {
        UpdateTrademark.maxLength = 25;
        UpdateTrademark.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }
}); 

// GLOBAL TABLES FUNCTIONS (MARCAS)
function openUpdateModal(id, nombre) {
    const UpdateTrademarkModal = document.getElementById('UpdateTrademarkModal');
    const UpdateTrademarkForm = document.getElementById('UpdateTrademarkForm');
    const closeUpdateTrademarkBtn = document.getElementById('closeUpdateTrademarkBtn');
    const UpdateTrademark = document.getElementById('UpdateTrademark');
    if (UpdateTrademarkModal && UpdateTrademarkForm && UpdateTrademark && closeUpdateTrademarkBtn) {
        UpdateTrademarkForm.action = `/marcas/update_trademark/${id}`;
        UpdateTrademark.value = nombre;
        UpdateTrademarkModal.classList.add('active');
    }
     closeUpdateTrademarkBtn.addEventListener('click', () => UpdateTrademarkModal.classList.remove('active'));
}

function openDeleteModal(id) {
    const DeleteTrademarkModal = document.getElementById('DeleteTrademarkModal');
    const DeleteTrademarkForm = document.getElementById('DeleteTrademarkForm');
    const closeDeleteTrademarkBtn = document.getElementById('closeDeleteTrademarkBtn');
    const DeleteTrademark = document.getElementById('DeleteTrademark');
    if (DeleteTrademarkModal && DeleteTrademarkForm) {
        DeleteTrademarkForm.action = `/marcas/delete_trademark/${id}`;
        DeleteTrademarkModal.classList.add('active');   
    }
    closeDeleteTrademarkBtn.addEventListener('click', () => DeleteTrademarkModal.classList.remove('active'));
}