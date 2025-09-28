document.addEventListener('DOMContentLoaded', function() {
    const bouquetBlocks = document.querySelectorAll('.recommended__block');

    bouquetBlocks.forEach(block => {
        block.addEventListener('click', function() {
            const bouquetId = this.getAttribute('data-bouquet-id');
            window.location.href = `/card/${bouquetId}/`;
        });
    });
});