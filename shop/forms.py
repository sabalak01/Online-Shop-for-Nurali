from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CouponForm(forms.Form):
    coupon_code = forms.CharField(max_length=50)
