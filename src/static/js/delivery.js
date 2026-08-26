document.addEventListener('DOMContentLoaded', () => {
    const closeUpdateBtn = document.getElementById('closeUpdateDeliveryBtn');

    if (closeUpdateBtn) {
        closeUpdateBtn.addEventListener('click', () => {
            cerrarModalUpdateDelivery();
        });
    }


    window.addEventListener('click', (event) => {
        const updateModal = document.getElementById('UpdateDeliveryModal');
        const reportModal = document.getElementById('ReporteEntregasModal');

        if (event.target === updateModal) {
            cerrarModalUpdateDelivery();
        }
        if (event.target === reportModal) {
            cerrarModalReporteEntregas();
        }
    });
});


function openUpdateDeliveryModalFromBtn(buttonElement) {
    const id = buttonElement.getAttribute('data-id');
    const fecha = buttonElement.getAttribute('data-fecha');
    const estatus = buttonElement.getAttribute('data-estatus');
    
    openUpdateDeliveryModal(id, fecha, estatus);
}


function openUpdateDeliveryModal(id, fecha, estatus) {
    const modal = document.getElementById('UpdateDeliveryModal');
    const form = document.getElementById('UpdateDeliveryForm');
    const inputFecha = document.getElementById('FechaEntrega');
    const selectEstatus = document.getElementById('Estatus');

    if (form) {
        form.action = `/entregas/update/${id}`;
    }
    
    if (inputFecha && fecha) {
        inputFecha.value = fecha;
    }

    if (selectEstatus && estatus) {
        selectEstatus.value = estatus.trim();
    }

    if (modal) {
        modal.classList.add('active');
    }
}

function cerrarModalUpdateDelivery() {
    const modal = document.getElementById('UpdateDeliveryModal');
    if (modal) {
        modal.classList.remove('active');
    }
}


function abrirModalReporteEntregas() {
    const modal = document.getElementById('ReporteEntregasModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function cerrarModalReporteEntregas() {
    const modal = document.getElementById('ReporteEntregasModal');
    if (modal) {
        modal.classList.remove('active');
    }
}