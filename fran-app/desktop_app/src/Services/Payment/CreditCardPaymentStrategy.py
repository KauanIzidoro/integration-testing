from Services.Payment.PaymentStrategy import PaymentStrategy

class CreditCardPaymentStrategy(PaymentStrategy):
    def process_payment(self, total: float, **kwargs):
        return "Pagamento com cartão de crédito processado."
