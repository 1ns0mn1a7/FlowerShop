document.addEventListener('DOMContentLoaded', function() {
    const orderBtn = document.querySelector('.card__btn');

    if (orderBtn) {
        orderBtn.addEventListener('click', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const bouquetId = urlParams.get('bouquet_id') || window.location.pathname.split('/').filter(Boolean).pop();
            window.location.href = `/order/?bouquet_id=${bouquetId}`;
        });
    }
});