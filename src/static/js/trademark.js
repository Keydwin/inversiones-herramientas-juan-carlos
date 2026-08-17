document.addEventListener('DOMContentLoaded', () => {
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
})


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