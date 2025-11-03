from django.urls import path
from .views import *
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('index', index, name='index'),
    path('cart', cart, name='cart'),
    path('shop', shop, name='shop'),
    path('services', services, name='services'),
    path('thankyou', thankyou, name='thankyou'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('product_detail/<int:id>',product_detail),
    path('remove/<int:id>',remove),
    # path('checkout/',checkout),
    path('signup',signup),
    path('logins',logins),
    path('checkout', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    # path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),

    # # Cart operations
    # path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('delete-cart-item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)