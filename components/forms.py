from django import forms
from .models import Component, Category, MaintenanceLog, ComponentCheckout
from django.core.exceptions import ValidationError

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'category', 'description', 'serial_number', 'quantity',
                 'status', 'location', 'purchase_date', 'last_maintenance_date', 
                 'next_maintenance_date', 'image']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'last_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serial_number'].required = False
        self.fields['last_maintenance_date'].required = False
        self.fields['next_maintenance_date'].required = False
        self.fields['image'].required = False

class MaintenanceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['maintenance_date', 'description']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ComponentCheckoutForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        help_text="Enter the number of components to checkout"
    )
    user_name = forms.CharField(
        max_length=100,
        help_text="Enter your full name",
        required=False  # Make it optional since we'll use the user's name by default
    )
    
    class Meta:
        model = ComponentCheckout
        fields = ['user_name', 'quantity', 'user_branch', 'user_phone', 'user_email', 'expected_return_date', 'notes']
        widgets = {
            'expected_return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.component = kwargs.pop('component', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['user_email'].initial = self.user.email
            self.fields['user_name'].initial = self.user.get_full_name() or self.user.username

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if self.component and quantity > self.component.quantity:
            raise ValidationError(f"Cannot checkout more than available quantity ({self.component.quantity} available)")
        return quantity 