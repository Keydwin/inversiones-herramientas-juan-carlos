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
    document.addEventListener('submit', (e) => {
        // Select all form controls
        const formControls = e.target.querySelectorAll(
            'input[type="text"], input[type="number"], input:not([type]), textarea, select'
        );
        
        let isFormInvalid = false;

        formControls.forEach(control => {
            // Check if field is optional
            if (control.classList.contains('opcional')) {
                control.value = control.value.trim();
                return;
            }

            // Select elements
            if (control.tagName.toLowerCase() === 'select') {
                if (control.value === '' || control.value === '0') {
                    isFormInvalid = true;
                }
            } 
            // Number inputs
            else if (control.type === 'number') {
                if (control.value === '' || parseFloat(control.value) < 0) {
                    isFormInvalid = true;
                }
            } 
            // Text inputs and textareas
            else {
                const cleanValue = control.value.trim();
                if (cleanValue === '') {
                    isFormInvalid = true;
                    control.value = ''; 
                } else {
                    control.value = cleanValue; 
                }
            }
        });

        // Block submit silently
        if (isFormInvalid) {
            e.preventDefault();
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
            
        }, 3000);
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
        UpdateTrademarkForm.action = `/update_trademark/${id}`;
        
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
        DeleteTrademarkForm.action = `/delete_trademark/${id}`;
        
        // We inject the trademark name into a text label so the user knows what they are deleting
        DeleteTrademark.textContent = nombre;
        
        // We show the delete modal using your style
        DeleteTrademarkModal.classList.add('active');
    }
}