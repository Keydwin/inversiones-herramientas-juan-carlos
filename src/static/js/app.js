document.addEventListener('DOMContentLoaded', () => {
    
    // ELEMENTS OF THE DOM
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const dropdowns = document.querySelectorAll('.dropdown-toggle');

    // SUBMENU CONTROL
    dropdowns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // WE LOOK FOR THE SUBMENU THAT IS RIGHT AFTER THE BUTTON
            const submenu = btn.nextElementSibling;
            
            // WE CLOSE OTHER OPEN SUBMENUS
            document.querySelectorAll('.submenu').forEach(sub => {
                if (sub !== submenu) {
                    sub.classList.remove('show');
                    sub.previousElementSibling.classList.remove('dropdown-open');
                }
            });

            // WE OPEN/CLOSE THE CURRENT ONE
            submenu.classList.toggle('show');
            btn.classList.toggle('dropdown-open');
        });
    });

    // OPENING/CLOSING THE SIDE MENU
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });



// GLOBAL VALIDATOR 
    let errorTimeout = null; 

    document.addEventListener('submit', (e) => {
        const currentForm = e.target;
        const formControls = currentForm.querySelectorAll(
            'input[type="text"], input[type="number"], input:not([type]), textarea, select'
        );
        
        let isFormInvalid = false;
        const errorSummary = currentForm.querySelector('.form-error');

        // Initial cleanup before re-validation
        if (errorSummary) {
            errorSummary.textContent = "";
            errorSummary.classList.remove('active');
        }
        if (errorTimeout) {
            clearTimeout(errorTimeout); // Cancel any active previous timer
        }

        formControls.forEach(control => {
            if (control.classList.contains('opcional')) {
                control.value = control.value.trim();
                return;
            }

            control.classList.remove('input-error-border');

            // Validations
            if (control.tagName.toLowerCase() === 'select') {
                if (control.value === '' || control.value === '0') {
                    isFormInvalid = true;
                    control.classList.add('input-error-border');
                }
            } 
            else if (control.type === 'number') {
                if (control.value === '' || parseFloat(control.value) < 0) {
                    isFormInvalid = true;
                    control.classList.add('input-error-border');
                }
            } 
            else {
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

        // If the form has errors
        if (isFormInvalid) {
            e.preventDefault(); // Stop the form submission to Flask
            
            if (errorSummary) {
                errorSummary.textContent = "Por favor ingrese todos los datos solicitados";
                errorSummary.classList.add('active');

                // TIMER 
                errorTimeout = setTimeout(() => {
                    errorSummary.classList.remove('active');
                    
                    // Wait for the close animation (250ms) to clear the text
                    setTimeout(() => {
                        if (!errorSummary.classList.contains('active')) {
                            errorSummary.textContent = ""; 
                        }
                    }, 250);

                    // Remove red borders when the error message fades out
                    formControls.forEach(c => c.classList.remove('input-error-border'));
                }, 4000); 
            }
        }
    });

    // INTERACTIVE CLEANUP ON TYPE
    document.addEventListener('input', (e) => {
        const control = e.target;
        control.classList.remove('input-error-border');
        
        const currentForm = control.closest('form');
        if (currentForm) {
            const errorSummary = currentForm.querySelector('.form-error');
            if (errorSummary) {
                errorSummary.classList.remove('active');
                
                // Clear text after interactive close
                setTimeout(() => {
                    if (!errorSummary.classList.contains('active')) {
                        errorSummary.textContent = ""; 
                    }
                }, 250);
            }
        }
        if (errorTimeout) {
            clearTimeout(errorTimeout);
        }
    });
    
    document.addEventListener('click', (e) => {
            // Check if the click was on a cancel button
            const cancelBtn = e.target.closest('.btn-cancel');
            
            if (cancelBtn) {
                // Find the parent modal to get the form
                const modal = cancelBtn.closest('.modal-overlay');
                if (modal) {
                    const form = modal.querySelector('form');
                    if (form) {
                        // Clean and hide the error text container
                        const errorSummary = form.querySelector('.form-error');
                        if (errorSummary) {
                            errorSummary.textContent = "";
                            errorSummary.classList.remove('active');
                        }
                        
                        // Remove all red borders from inputs, textareas, and selects
                        const inputs = form.querySelectorAll('input, textarea, select');
                        inputs.forEach(input => {
                            input.classList.remove('input-error-border');
                        });
                    }
                }
            }
        });


    // FLASH
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            
            setTimeout(() => {
                alert.remove();
            }, 500); 
            
        }, 2000);
    });



    // MODAL REGISTRAR
    const openTrademarkModalBtn = document.getElementById('openTrademarkModalBtn');
    const closeTrademarkBtn = document.getElementById('closeTrademarkBtn');
    const TrademarkModal = document.getElementById('TrademarkModal');
    const TrademarkForm = document.getElementById('TrademarkForm');
    const trademarkInput = document.getElementById('Marca');

    // MODAL MODIFICAR
    const UpdateTrademarkModal = document.getElementById('UpdateTrademarkModal');
    const closeUpdateTrademarkBtn = document.getElementById('closeUpdateTrademarkBtn');
    const UpdateTrademarkForm = document.getElementById('UpdateTrademarkForm');
    const UpdateTrademark = document.getElementById('UpdateTrademark');

    // MODAL ELIMINAR
    const DeleteTrademarkModal = document.getElementById('DeleteTrademarkModal');
    const closeDeleteTrademarkBtn = document.getElementById('closeDeleteTrademarkBtn');
    const DeleteTrademarkForm = document.getElementById('DeleteTrademarkForm');
    const DeleteTrademark = document.getElementById('DeleteTrademark');
    
    // OPEN TRADEMARK MODAL WINDOW
    openTrademarkModalBtn.addEventListener('click', () => {
        TrademarkForm.reset(); // CLEAR INPUTS UPON OPENING
        TrademarkModal.classList.add('active');
    });

    // CLOSE TRADEMARK MODAL WINDOW
    closeTrademarkBtn.addEventListener('click', () => {
        TrademarkModal.classList.remove('active');
    });

    // CLOSE UPDATE TRADEMARK MODAL WINDOW
    closeUpdateTrademarkBtn.addEventListener('click', () => {
        UpdateTrademarkModal.classList.remove('active');
    });

    // CLOSE DELETE TRADEMARK MODAL WINDOW
    closeDeleteTrademarkBtn.addEventListener('click', () => {
        DeleteTrademarkModal.classList.remove('active');
    });

    if (trademarkInput) {
        trademarkInput.maxLength = 30;
        trademarkInput.addEventListener('input', (e) => {

            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    if (trademarkInput) {
            UpdateTrademark.maxLength = 30;
            UpdateTrademark.addEventListener('input', (e) => {

                e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
            });
        }

}); 


// GLOBAL FUNCTION TO OPEN UPDATE MODAL FROM THE TABLE
function openUpdateModal(id, nombre) {
    const UpdateTrademarkModal = document.getElementById('UpdateTrademarkModal');
    const UpdateTrademarkForm = document.getElementById('UpdateTrademarkForm');
    const UpdateTrademark = document.getElementById('UpdateTrademark');

    if (UpdateTrademarkModal && UpdateTrademarkForm && UpdateTrademark) {
        // We set the dynamic Flask URL with IdMarca
        UpdateTrademarkForm.action = `/marcas/update_trademark/${id}`;
        
        // We put the current trademark name inside the input
        UpdateTrademark.value = nombre;
        
        // We show the update modal using your style
        UpdateTrademarkModal.classList.add('active');
    }
}

// GLOBAL FUNCTION TO OPEN DELETE MODAL FROM THE TABLE
function openDeleteModal(id, nombre) {
    const DeleteTrademarkModal = document.getElementById('DeleteTrademarkModal');
    const DeleteTrademarkForm = document.getElementById('DeleteTrademarkForm');
    const DeleteTrademark = document.getElementById('DeleteTrademark');

    if (DeleteTrademarkModal && DeleteTrademarkForm && DeleteTrademark) {
        // We set the dynamic Flask URL with IdMarca
        DeleteTrademarkForm.action = `/marcas/delete_trademark/${id}`;
        
        // We inject the trademark name into a text label so the user knows what they are deleting
        DeleteTrademark.textContent = nombre;
        
        // We show the delete modal using your style
        DeleteTrademarkModal.classList.add('active');
    }
}