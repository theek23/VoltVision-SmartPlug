from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Customer

def create_customer(request):
    # Create a new customer
    customer = Customer(name='John Doe', email='john@example.com', age=30)
    customer.save()

    # Optionally, retrieve all customers
    all_customers = Customer.objects.all()

    # Render a template or return a response
    return render(request, 'myapp/customer_list.html', {'customers': all_customers})
