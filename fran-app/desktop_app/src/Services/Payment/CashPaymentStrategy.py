from Services.Payment.PaymentStrategy import PaymentStrategy

class CashPaymentStrategy(PaymentStrategy):
    def process_payment(self, total: float, **kwargs):
        valor_pago = kwargs.get('valor_pago', 0.0)
        if valor_pago < total:
            raise ValueError("Valor pago é insuficiente.")
        troco = valor_pago - total
        return f"Pagamento em dinheiro processado. Troco: R$ {troco:.2f}"
