document.addEventListener('DOMContentLoaded', function() {
    const backBtn = document.querySelector('.order__form_btn');
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            const backUrl = this.getAttribute('data-back-url');
            const bouquetId = this.getAttribute('data-bouquet-id');
            window.location.href = backUrl + '?bouquet_id=' + bouquetId;
        });
    }
});