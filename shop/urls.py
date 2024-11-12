from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


app_name = 'shop'

urlpatterns = [
    path('',views.home,name='home'),
    path('products', views.product_list,name='product_list'),
    path('category/<int:category_id>/',views.category_products,name='category_products'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)