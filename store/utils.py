import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cart = {}
        print('Cart is not valid JSON')

    print('CART:', cart)  # Debugging the cart data

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)

            if not product.digital:
                order['shipping'] = True

        except Product.DoesNotExist:
            print(f'Product with id {i} does not exist.')
        except Exception as e:
            print(f'Error processing cart item {i}: {str(e)}')

    print('Final Cookie Cart Data:', {'cartItems': cartItems, 'order': order, 'items': items})
    return {'cartItems': cartItems, 'order': order, 'items': items}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    print('Cart Data:', {'items': items, 'order': order, 'cartItems': cartItems})  # Debugging
    return {'items': items, 'order': order, 'cartItems': cartItems}



def guestOrder(request, data):
    print('User is not logged in...')
    print('COOKIES:', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        print('Processing item:', item)
        try:
            product = Product.objects.get(id=item['product']['id'])
            print(f'Found product: {product}')
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
            print(f'Created order item: {order_item}')
        except Product.DoesNotExist:
            print(f'Product with id {item["product"]["id"]} does not exist.')
        except Exception as e:
            print(f'Error creating order item: {str(e)}')
        return customer, order

