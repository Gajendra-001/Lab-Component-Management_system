from django.contrib import admin
from .models import Category, Component, MaintenanceLog, ComponentCheckout

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'location', 'created_by', 'created_at')
    list_filter = ('status', 'category', 'created_by')
    search_fields = ('name', 'serial_number', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'serial_number', 'status', 'location')
        }),
        ('Dates', {
            'fields': ('purchase_date', 'last_maintenance_date', 'next_maintenance_date')
        }),
        ('Additional Information', {
            'fields': ('image', 'created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('component', 'maintenance_date', 'performed_by')
    list_filter = ('maintenance_date', 'performed_by')
    search_fields = ('component__name', 'description')
    readonly_fields = ('created_at',)

@admin.register(ComponentCheckout)
class ComponentCheckoutAdmin(admin.ModelAdmin):
    list_display = ('component', 'checked_out_by', 'checkout_date', 'expected_return_date', 'actual_return_date')
    list_filter = ('checkout_date', 'expected_return_date', 'actual_return_date', 'checked_out_by')
    search_fields = ('component__name', 'notes')
    readonly_fields = ('checkout_date',)
