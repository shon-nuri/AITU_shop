from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('store/category/<str:category>/', views.store_by_category, name='store_by_category'), 
    path('store/search', views.product_search, name='product_search'),
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('checkout/', views.checkout, name='checkout'),
    path('processOrder/', views.processOrder, name='processOrder'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),  
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'), 
    path('accounts/', include('accounts.urls')),
]
