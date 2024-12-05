from Services.Payment.PaymentStrategy import PaymentStrategy

class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def process(self, total: float, **kwargs):
        return self._strategy.process_payment(total, **kwargs)
