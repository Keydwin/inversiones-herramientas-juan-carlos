document.addEventListener('DOMContentLoaded', () => {
    
    // ELEMENTS OF THE DOM
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    const openTrademarkModalBtn = document.getElementById('openTrademarkModalBtn');
    const closeTrademarkBtn = document.getElementById('closeTrademarkBtn');
    const TrademarkModal = document.getElementById('TrademarkModal');
    const TrademarkForm = document.getElementById('TrademarkForm');
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    const trademarkInput = document.getElementById('Marca');

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



        // OPEN TRADEMARK MODAL WINDOW
        openTrademarkModalBtn.addEventListener('click', () => {
            TrademarkForm.reset(); // CLEAR INPUTS UPON OPENING
            TrademarkModal.classList.add('active');
        });

        // CLOSE TRADEMARK MODAL WINDOW
        closeTrademarkBtn.addEventListener('click', () => {
            TrademarkModal.classList.remove('active');
        });

        // TRADEMARK input
        if (trademarkInput) {

            trademarkInput.maxLength = 30;

            trademarkInput.addEventListener('input', (e) => {

                    const invalidCharacters = /[^A-Za-zÁéíóúÁÉÍÓÚñÑ ]/g;
                
                if (invalidCharacters.test(e.target.value)) {
                    e.target.value = e.target.value.replace(invalidCharacters, '');
                }
            });

    }
});