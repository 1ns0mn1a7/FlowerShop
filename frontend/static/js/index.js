document.addEventListener('DOMContentLoaded', function () {
    const quizButton = document.querySelector('.banner__btn')
    const popup = document.getElementById('successPopup');
    if(quizButton){
        quizButton.addEventListener('click', function () {
            window.location.href = "/quiz";
        })
    }

     if (popup) {
        setTimeout(closePopup, 8000);

        popup.addEventListener('click', function(e) {
            if (e.target === this) {
                closePopup();
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && popup.style.display === 'flex') {
                closePopup();
            }
        });
    }


    function closePopup() {
        const popup = document.getElementById('successPopup');
        if (popup) {
            popup.style.animation = 'popupDisappear 0.3s ease-in forwards';
            setTimeout(() => {
                popup.style.display = 'none';
            }, 300);
        }
    }

})