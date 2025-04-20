from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFilter, NumberFilter
from .models import Component

class ComponentFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    category = CharFilter(field_name='category__name', lookup_expr='icontains')
    status = ChoiceFilter(choices=Component.STATUS_CHOICES)
    serial_number = CharFilter(lookup_expr='icontains')
    location = CharFilter(lookup_expr='icontains')
    quantity_min = NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_max = NumberFilter(field_name='quantity', lookup_expr='lte')
    purchase_date_after = DateFilter(field_name='purchase_date', lookup_expr='gte')
    purchase_date_before = DateFilter(field_name='purchase_date', lookup_expr='lte')

    class Meta:
        model = Component
        fields = ['name', 'category', 'status', 'serial_number', 'location', 
                 'quantity_min', 'quantity_max', 'purchase_date_after', 'purchase_date_before'] 