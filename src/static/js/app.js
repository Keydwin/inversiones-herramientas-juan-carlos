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

    
}); 