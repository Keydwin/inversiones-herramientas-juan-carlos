document.addEventListener('DOMContentLoaded', () => {
    
    // ELEMENTS OF THE DOM
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    const openTrademarkModalBtn = document.getElementById('openTrademarkModalBtn');
    const closeTrademarkBtn = document.getElementById('closeTrademarkBtn');
    const TrademarkModal = document.getElementById('TrademarkModal');
    const TrademarkForm = document.getElementById('TrademarkForm');
    const searchInput = document.getElementById('searchInput');
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    const trademarkSearch = document.getElementById('trademarkSearch');

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

    // PRODUCT MODAL WINDOW SWITCHES

        // OPEN PRODUCT MODAL WINDOW
        openTrademarkModalBtn.addEventListener('click', () => {
            TrademarkForm.reset(); // CLEAR INPUTS UPON OPENING
            TrademarkModal.classList.add('active');
        });

        // CLOSE PRODUCT MODAL WINDOW
        closeTrademarkBtn.addEventListener('click', () => {
            TrademarkModal.classList.remove('active');
        });



    // SEARCH FILTER FOR TRADEMARKS
    if (trademarkSearch) {
        trademarkSearch.addEventListener('keyup', () => {
            const filterValue = trademarkSearch.value.toLowerCase();
            // Select all rows in the table body
            const tableRows = document.querySelectorAll('.data-table tbody tr');

            tableRows.forEach(row => {
                // We get the text from the first cell
                const trademarkCell = row.querySelector('td');
                
                if (trademarkCell) {
                    const trademarkText = trademarkCell.textContent.toLowerCase();
                    
                    // If the brand text contains what we wrote, it is displayed; if not, it is hidden.
                    if (trademarkText.includes(filterValue)) {
                        row.style.display = "";
                    } else {
                        row.style.display = "none";
                    }
                }
            });
        });
    }
})