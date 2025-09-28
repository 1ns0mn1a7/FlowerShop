document.addEventListener('DOMContentLoaded', function() {
    const backBtn = document.querySelector('.order__form_btn');
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            const backUrl = this.getAttribute('data-back-url');
            const bouquetId = this.getAttribute('data-bouquet-id');
            window.location.href = backUrl + '?bouquet_id=' + bouquetId;
        });
    }

    const metaTag = document.querySelector('meta[name="stripe-publishable-key"]');
    const stripePublishableKey = metaTag ? metaTag.getAttribute('content') : null;
    // const stripePublishableKey = "{{ STRIPE_PUBLISHABLE_KEY }}";
    console.log("AAA",stripePublishableKey)
    if (!stripePublishableKey) {
        console.error('Stripe Publishable Key не найден.');
        return;
    }

    if (typeof Stripe === 'undefined') {
        console.error('Stripe.js не загружен');
        return;
    }

    initializeStripe(stripePublishableKey);

    function initializeStripe(publishableKey) {
        const stripe = Stripe(publishableKey);
        const elements = stripe.elements();

        const style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };

        const card = elements.create('card', {
            style: style,
            hidePostalCode: true
        });

        const cardElement = document.getElementById('card-element');
        if (cardElement) {
            card.mount('#card-element');

            card.addEventListener('change', ({error}) => {
                const displayError = document.getElementById('card-errors');
                if (error) {
                    displayError.textContent = error.message;
                } else {
                    displayError.textContent = '';
                }
            });
        } else {
            console.error('Элемент card-element не найден');
        }

        const form = document.getElementById('payment-form');
        if (form) {
            form.addEventListener('submit', async (event) => {
                event.preventDefault();

                const submitButton = document.getElementById('submit-button');
                const buttonText = document.getElementById('button-text');
                const spinner = document.getElementById('spinner');

                if (submitButton && buttonText && spinner) {
                    submitButton.disabled = true;
                    buttonText.style.display = 'none';
                    spinner.style.display = 'block';
                }

                try {
                    const { paymentMethod, error } = await stripe.createPaymentMethod({
                        type: 'card',
                        card: card,
                    });

                    if (error) {
                        const errorElement = document.getElementById('card-errors');
                        if (errorElement) {
                            errorElement.textContent = error.message;
                        }

                        if (submitButton && buttonText && spinner) {
                            submitButton.disabled = false;
                            buttonText.style.display = 'block';
                            spinner.style.display = 'none';
                        }
                    } else {
                        const tokenInput = document.createElement('input');
                        tokenInput.setAttribute('type', 'hidden');
                        tokenInput.setAttribute('name', 'stripeToken');
                        tokenInput.setAttribute('value', paymentMethod.id);
                        form.appendChild(tokenInput);

                        form.submit();
                    }
                } catch (error) {
                    console.error('Ошибка при создании платежного метода:', error);

                    if (submitButton && buttonText && spinner) {
                        submitButton.disabled = false;
                        buttonText.style.display = 'block';
                        spinner.style.display = 'none';
                    }
                }
            });
        }
    }
});