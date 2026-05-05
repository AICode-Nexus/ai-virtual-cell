// Matrix cell click interaction
document.addEventListener('DOMContentLoaded', function() {
    const matrixCells = document.querySelectorAll('.matrix-cell');
    const tableRows = document.querySelectorAll('.mapping-matrix-table tbody tr');

    // Create a mapping from bio+ai to table row
    const cellToRowMap = new Map();
    tableRows.forEach((row, index) => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 2) {
            const bio = cells[0].textContent.trim();
            const ai = cells[1].textContent.trim();
            const key = `${bio}|${ai}`;
            cellToRowMap.set(key, row);
        }
    });

    // Add click handlers to matrix cells
    matrixCells.forEach(cell => {
        const bio = cell.getAttribute('data-bio');
        const ai = cell.getAttribute('data-ai');
        const isEmpty = cell.classList.contains('mapping-empty');

        if (!isEmpty && bio && ai) {
            cell.style.cursor = 'pointer';

            cell.addEventListener('click', function() {
                const key = `${bio}|${ai}`;
                const targetRow = cellToRowMap.get(key);

                if (targetRow) {
                    // Smooth scroll to the row
                    targetRow.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });

                    // Highlight the row temporarily
                    targetRow.style.background = 'rgba(84,169,255,0.2)';
                    setTimeout(() => {
                        targetRow.style.background = '';
                    }, 2000);
                }
            });
        } else if (isEmpty) {
            // Empty cells show a tooltip
            cell.style.cursor = 'help';
            cell.setAttribute('title', `${bio} × ${ai}: 空白区域 - 潜在的创新机会`);
        }
    });

    // Add hover effect to show which row corresponds to hovered cell
    matrixCells.forEach(cell => {
        const bio = cell.getAttribute('data-bio');
        const ai = cell.getAttribute('data-ai');

        cell.addEventListener('mouseenter', function() {
            const key = `${bio}|${ai}`;
            const targetRow = cellToRowMap.get(key);

            if (targetRow) {
                targetRow.style.outline = '2px solid rgba(84,169,255,0.5)';
            }
        });

        cell.addEventListener('mouseleave', function() {
            const key = `${bio}|${ai}`;
            const targetRow = cellToRowMap.get(key);

            if (targetRow) {
                targetRow.style.outline = '';
            }
        });
    });
});
