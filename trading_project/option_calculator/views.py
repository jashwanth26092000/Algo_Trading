from django.shortcuts import render
from .forms import TradingForm
from decimal import Decimal

def calculate(request):
    form = TradingForm(request.POST or None)
    result = None
    message = None

    if form.is_valid():
        stock_price = Decimal(form.cleaned_data['stock_price'])
        option_premium = Decimal(form.cleaned_data['option_premium'])
        stop_loss = Decimal(form.cleaned_data['stop_loss'])
        target_price = Decimal(form.cleaned_data['target_price'])
        delta = Decimal(form.cleaned_data['delta'])
        risk_reward_ratio = Decimal(form.cleaned_data['risk_reward_ratio'])

        # Calculate stop loss and target premium
        stop_loss_premium = option_premium - delta * (stock_price - stop_loss)
        target_premium = option_premium + delta * (target_price - stock_price)
        
        # Calculate risk-reward
        risk = option_premium - stop_loss_premium
        reward = target_premium - option_premium
        expected_return = (reward * Decimal('0.5')) - (risk * Decimal('0.5'))
        
        # Calculate the target stock price based on the risk-reward ratio
        required_target_stock_price = stock_price + (reward * risk_reward_ratio)
        
        # Message about target price
        if target_price < required_target_stock_price:
            message = f"🔴 Target too low; adjust. Required target price: ₹{required_target_stock_price}"
        else:
            message = "✅ Target is good!"

        result = {
            'stop_loss_premium': stop_loss_premium,
            'target_premium': target_premium,
            'risk': risk,
            'reward': reward,
            'expected_return': expected_return,
            'required_target_stock_price': required_target_stock_price,
            'message': message,
        }

    return render(request, 'calculate.html', {'form': form, 'result': result})
