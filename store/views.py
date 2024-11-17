from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q, F
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.db.models import Avg


from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import *
import json, datetime, stripe, base64

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, 'store/index.html')

def store(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
    else:
        customer = None
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/checkout.html', context)

@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, _ = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

stripe.api_key = 'sk_test_51QAV8yP5U5NCIsrZ4FOSahWdDYqZx98QZdcSTwTKnEf6pV0N42YMsOM3nfJW6ZltMWGM7NjhWojlCaH9CaGw26EQ00rdObKkZq'
@csrf_exempt
def processOrder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data['items']

            # Create Stripe line items from cart data
            line_items = [
                {
                    'price_data': {
                        'currency': 'kzt',
                        'product_data': {
                            'name': item['name'],
                        },
                        'unit_amount': int(item['price'] * 100),  # Stripe expects amount in cents
                    },
                    'quantity': item['quantity'],
                }
                for item in items
            ]

            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )

            return JsonResponse({'url': session.url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_items = data.get('items', [])
            line_items = [
                {
                    'price_data': {
                        'currency': 'kzt',
                        'product_data': {'name': item['name']},
                        'unit_amount': int(item['price'] * 100),
                    },
                    'quantity': item['quantity'],
                } for item in cart_items
            ]

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )
            return JsonResponse({'url': session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def user_logout(request):
    logout(request)
    return redirect('index')

def payment_success(request):
    return render(request, 'store/success.html')

# View to render a cancel page if payment was canceled
def payment_cancel(request):
    return render(request, 'store/cancel.html')

@login_required(login_url='login')
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('reviews'), pk=pk)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    # Fetch related products from the same category
    same_category_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]

    # Fetch products on sale
    sale_products = Product.objects.filter(Q(sale_price__isnull=False) & Q(sale_price__lt=F('price')))[:4]

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'same_category_products': same_category_products,
        'sale_products': sale_products,
    }
    return render(request, 'store/product_detail.html', context)

def store_by_category(request, category):
    # Filter products by category
    products = Product.objects.filter(category__iexact=category)  # Case-insensitive match
    data = cartData(request)
    cartItems = data['cartItems']
    context = {
        'products': products,
        'category': category.capitalize(),
        'cartItems': cartItems  
    }
    return render(request, 'store/store.html', context)

def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    form = SearchForm(initial={'query': query})
    return render(request, 'store/store.html', {'form': form, 'products': products})