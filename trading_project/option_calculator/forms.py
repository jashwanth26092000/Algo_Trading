from django import forms

class TradingForm(forms.Form):
    stock_price = forms.DecimalField(
        label='Stock Price (₹)',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )
    option_premium = forms.DecimalField(
        label='Option Premium (₹)',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )
    delta = forms.DecimalField(
        label='Delta',
        max_digits=5,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    target_price = forms.DecimalField(
        label='Target Price (₹)',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )

    stop_loss = forms.DecimalField(
        label='Stop Loss (₹)',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )
   
    risk_reward_ratio = forms.IntegerField(
        label='Risk-to-Reward Ratio(1:3(default))',
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'},),
    
    )
