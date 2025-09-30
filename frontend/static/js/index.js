function closePopup() {
		const popup = document.getElementById('successPopup');
		if (popup) {
			popup.style.animation = 'popupDisappear 0.3s ease-in forwards';
			setTimeout(() => {
				popup.style.display = 'none';
			}, 300);
		}
	}

	document.addEventListener('DOMContentLoaded', function () {
		const quizButton = document.querySelector('.banner__btn');
		const popup = document.getElementById('successPopup');

		// Назначаем обработчики для кнопок закрытия
		const closeButtons = document.querySelectorAll('.popup-close, .popup-btn');
		closeButtons.forEach(button => {
			button.addEventListener('click', closePopup);
		});

		if(quizButton){
			quizButton.addEventListener('click', function () {
				window.location.href = "/quiz";
			});
		}

		if (popup) {
			// Автоматическое закрытие через 8 секунд
			setTimeout(closePopup, 8000);

			// Закрытие по клику на фон
			popup.addEventListener('click', function(e) {
				if (e.target === this) {
					closePopup();
				}
			});

			// Закрытие по Escape
			document.addEventListener('keydown', function(e) {
				if (e.key === 'Escape' && popup.style.display === 'flex') {
					closePopup();
				}
			});
		}
	});