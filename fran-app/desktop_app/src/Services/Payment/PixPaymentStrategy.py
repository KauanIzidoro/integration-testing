from Services.Payment.PaymentStrategy import PaymentStrategy

class PixPaymentStrategy(PaymentStrategy):
    def process_payment(self, total: float, **kwargs):
        return "Pagamento via Pix processado com sucesso."
