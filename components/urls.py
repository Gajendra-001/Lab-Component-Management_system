from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('components/', views.ComponentListView.as_view(), name='component-list'),
    path('inventory/', views.InventoryListView.as_view(), name='inventory-list'),
    path('component/<int:pk>/', views.ComponentDetailView.as_view(), name='component-detail'),
    path('component/new/', views.ComponentCreateView.as_view(), name='component-create'),
    path('component/<int:pk>/update/', views.ComponentUpdateView.as_view(), name='component-update'),
    path('component/<int:pk>/delete/', views.ComponentDeleteView.as_view(), name='component-delete'),
    path('component/<int:pk>/maintenance/', views.add_maintenance_log, name='add-maintenance-log'),
    path('component/<int:pk>/checkout/', views.checkout_component, name='checkout-component'),
    path('component/<int:pk>/return/', views.return_component, name='return-component'),
    path('component/<int:pk>/status/', views.component_status_update, name='component-status-update'),
    path('component/<int:pk>/update-status/', views.update_component_status, name='component-update-status'),
    path('search/', views.search_components, name='search-components'),
] 