document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.consultation__form');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Отправка...';
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = {
            client_name: formData.get('fname'),
            client_phone: formData.get('tel')
        };

        try {
            const response = await fetch('/api/consultations/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                showMessage('Заявка успешно отправлена!', 'success');
                form.reset();
            } else {
                showMessage('Произошла ошибка при отправке заявки', 'error');
            }
        } catch (error) {
            showMessage('Ошибка соединения', 'error');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });

    function showMessage(text, type) {
        const message = document.createElement('div');
        message.textContent = text;
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            z-index: 1000;
            font-family: Arial, sans-serif;
            ${type === 'success' ? 'background: green;' : 'background: red;'}
        `;
        document.body.appendChild(message);

        setTimeout(() => {
            message.remove();
        }, 3000);
    }
});