from django.db import models

class Back_Test_Trade(models.Model):
    TRADE_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.trade_type} {self.quantity} {self.ticker} at {self.price}'
