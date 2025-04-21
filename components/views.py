from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Component, Category, MaintenanceLog, ComponentCheckout
from .forms import ComponentForm, MaintenanceLogForm, ComponentCheckoutForm
from django_filters.views import FilterView
from .filters import ComponentFilter
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
def home(request):
    # Get all components with their checkouts
    components = Component.objects.prefetch_related('checkouts').all()
    
    # Initialize counters
    total_quantity = 0
    available_quantity = 0
    in_use_quantity = 0
    maintenance_quantity = 0
    
    # Calculate quantities
    for component in components:
        # Get active checkouts
        active_checkouts = component.checkouts.filter(actual_return_date__isnull=True)
        in_use_count = sum(checkout.quantity for checkout in active_checkouts)
        
        if component.status == 'maintenance':
            maintenance_quantity += component.quantity
        else:
            # Available is what's left after checkouts
            available_count = max(0, component.quantity - in_use_count)
            available_quantity += available_count
            in_use_quantity += in_use_count
        
        # Total is the original quantity for each component
        total_quantity += component.quantity
    
    context = {
        'total_components': total_quantity,
        'available_components': available_quantity,
        'in_use_components': in_use_quantity,
        'maintenance_components': maintenance_quantity,
        'recent_checkouts': ComponentCheckout.objects.select_related('component', 'checked_out_by').order_by('-checkout_date')[:5],
        'recent_maintenance': MaintenanceLog.objects.select_related('component', 'performed_by').order_by('-maintenance_date')[:5],
    }
    return render(request, 'components/home.html', context)

class ComponentListView(LoginRequiredMixin, ListView):
    model = Component
    template_name = 'components/component_list.html'
    context_object_name = 'components'
    paginate_by = 12

    def get_queryset(self):
        queryset = Component.objects.all().prefetch_related(
            'checkouts'
        ).select_related(
            'category', 'created_by'
        ).order_by('category__name', 'name')
        
        status = self.request.GET.get('status')
        if status in ['available', 'in_use', 'maintenance']:
            queryset = queryset.filter(status=status)
        
        # Annotate each component with its latest checkout information
        for component in queryset:
            component.latest_checkout = component.checkouts.filter(
                actual_return_date__isnull=True
            ).first()
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate total components by summing available and in-use quantities
        components = Component.objects.prefetch_related('checkouts').all()
        
        total_quantity = 0
        available_quantity = 0
        in_use_quantity = 0
        maintenance_quantity = 0
        
        for component in components:
            # Get active checkouts
            active_checkouts = component.checkouts.filter(actual_return_date__isnull=True)
            in_use_count = sum(checkout.quantity for checkout in active_checkouts)
            
            if component.status == 'maintenance':
                maintenance_quantity += component.quantity
            else:
                # Available is what's left after checkouts
                available_count = max(0, component.quantity - in_use_count)
                available_quantity += available_count
                in_use_quantity += in_use_count
            
            # Total is the original quantity for each component
            total_quantity += component.quantity
        
        context['total_components'] = total_quantity
        context['available_components'] = available_quantity
        context['in_use_components'] = in_use_quantity
        context['maintenance_components'] = maintenance_quantity
        return context

class InventoryListView(LoginRequiredMixin, FilterView):
    model = Component
    template_name = 'components/inventory.html'
    context_object_name = 'components'
    filterset_class = ComponentFilter
    paginate_by = 20

    def get_queryset(self):
        queryset = Component.objects.all().prefetch_related('checkouts').select_related('category').order_by('category__name', 'name')
        
        # Add search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(category__name__icontains=search_query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ComponentDetailView(LoginRequiredMixin, DetailView):
    model = Component
    template_name = 'components/component_detail.html'
    context_object_name = 'component'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = self.object
        
        # Get active checkouts
        active_checkouts = component.checkouts.filter(actual_return_date__isnull=True)
        in_use_count = sum(checkout.quantity for checkout in active_checkouts)
        
        # Calculate quantities
        if component.status == 'maintenance':
            context['maintenance_quantity'] = component.quantity
            context['in_use_quantity'] = 0
            context['available_quantity'] = 0
        else:
            context['maintenance_quantity'] = 0
            context['in_use_quantity'] = in_use_count
            context['available_quantity'] = max(0, component.quantity - in_use_count)
        
        context['maintenance_logs'] = component.maintenance_logs.all().order_by('-maintenance_date')
        context['checkout_history'] = component.checkouts.all().order_by('-checkout_date')
        return context

class ComponentCreateView(LoginRequiredMixin, CreateView):
    model = Component
    form_class = ComponentForm
    template_name = 'components/component_form.html'
    success_url = reverse_lazy('component-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Component added successfully!')
        return super().form_valid(form)

class ComponentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Component
    form_class = ComponentForm
    template_name = 'components/component_form.html'
    success_url = reverse_lazy('component-list')

    def form_valid(self, form):
        messages.success(self.request, 'Component updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        component = self.get_object()
        return self.request.user == component.created_by or self.request.user.is_staff

class ComponentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Component
    template_name = 'components/component_confirm_delete.html'
    success_url = reverse_lazy('component-list')

    def test_func(self):
        component = self.get_object()
        return self.request.user == component.created_by or self.request.user.is_staff

@login_required
def add_maintenance_log(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            maintenance_log = form.save(commit=False)
            maintenance_log.component = component
            maintenance_log.performed_by = request.user
            maintenance_log.save()
            messages.success(request, 'Maintenance log added successfully!')
            return redirect('component-detail', pk=pk)
    else:
        form = MaintenanceLogForm()
    return render(request, 'components/maintenance_log_form.html', {'form': form, 'component': component})

@login_required
def checkout_component(request, pk):
    component = get_object_or_404(Component, pk=pk)
    
    if request.method == 'POST':
        form = ComponentCheckoutForm(request.POST, user=request.user, component=component)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.component = component
            checkout.checked_out_by = request.user
            checkout.checkout_date = timezone.now()
            
            # Update component quantity
            quantity_to_checkout = form.cleaned_data['quantity']
            
            # Calculate currently checked out quantity
            active_checkouts = component.checkouts.filter(actual_return_date__isnull=True)
            currently_checked_out = sum(c.quantity for c in active_checkouts)
            available_quantity = component.quantity - currently_checked_out
            
            if quantity_to_checkout <= available_quantity:
                # Get entered name from form or fallback to user's name
                entered_name = form.cleaned_data.get('user_name') or request.user.get_full_name() or request.user.username
                
                # Save the display name
                checkout.display_name = entered_name
                
                # Save the checkout
                checkout.save()
                
                # Update status based on available quantity
                if available_quantity - quantity_to_checkout == 0:
                    component.status = 'in_use'
                    component.save()
                
                # Prepare email content
                context = {
                    'component': component,
                    'quantity': quantity_to_checkout,
                    'user_name': entered_name,
                    'expected_return_date': checkout.expected_return_date,
                }
                
                # Render email templates
                html_message = render_to_string('components/email/checkout_confirmation.html', context)
                plain_message = strip_tags(html_message)
                
                # Send email with user's name in the from field
                send_mail(
                    subject=f'Component Checkout Confirmation - {component.name}',
                    message=plain_message,
                    from_email=(entered_name, 'dhaked1415@gmail.com'),  # Use entered name here too
                    recipient_list=[checkout.user_email],
                    html_message=html_message,
                )
                
                messages.success(request, f'Successfully checked out {quantity_to_checkout} {component.name}(s)')
                return redirect('component-list')
            else:
                messages.error(request, f'Cannot checkout more than available quantity ({available_quantity} available)')
    else:
        form = ComponentCheckoutForm(user=request.user, component=component)
    
    context = {
        'form': form,
        'component': component,
    }
    return render(request, 'components/checkout_form.html', context)

@login_required
def return_component(request, pk):
    component = get_object_or_404(Component, pk=pk)
    checkout_id = request.GET.get('checkout_id')
    
    if checkout_id:
        # Return specific checkout
        checkout = get_object_or_404(ComponentCheckout, id=checkout_id, actual_return_date__isnull=True)
        
        # Mark the checkout as returned
        checkout.actual_return_date = timezone.now()
        checkout.save()
        
        # Check remaining active checkouts
        active_checkouts = component.checkouts.filter(actual_return_date__isnull=True)
        if not active_checkouts.exists():
            component.status = 'available'
            component.save()
            
        messages.success(request, f'Successfully returned {checkout.quantity} {component.name}(s)')
    else:
        # Return all active checkouts
        active_checkouts = component.checkouts.filter(actual_return_date__isnull=True)
        total_returned = 0
        
        for checkout in active_checkouts:
            total_returned += checkout.quantity
            checkout.actual_return_date = timezone.now()
            checkout.save()
        
        if total_returned > 0:
            component.status = 'available'
            component.save()
            messages.success(request, f'Successfully returned {total_returned} {component.name}(s)')
    
    return redirect('component-detail', pk=pk)

@login_required
def component_status_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['available', 'in_use']:
            component.status = new_status
            component.save()
            messages.success(request, f'Component status updated to {new_status}.')
    return redirect('component-list')

@login_required
def update_component_status(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['available', 'in_use', 'maintenance']:
            component.status = new_status
            component.save()
            messages.success(request, f'Component status updated to {new_status}.')
    return redirect('component-detail', pk=pk)

def search_components(request):
    query = request.GET.get('q', '')
    if query:
        components = Component.objects.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query)
        ).select_related('category')[:10]
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request - return JSON
            data = [{
                'id': component.id,
                'name': component.name,
                'category': component.category.name
            } for component in components]
            return JsonResponse({'components': data}, safe=False)
        else:
            # Regular request - render template
            return render(request, 'components/inventory.html', {
                'components': components,
                'search_query': query
            })
    return JsonResponse({'components': []}, safe=False)
