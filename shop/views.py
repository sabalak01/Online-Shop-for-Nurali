from itertools import product
from lib2to3.fixes.fix_input import context

from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Category, Cart, CartProduct



def home(request):
    return render(request,'shop/home.html')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories':categories}
    return render(request,'shop/product_list.html',context)

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'shop/category_products.html', {'products':products, 'category':category})

def cart_view(request):
    cart, _ = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    request.session['cart_id'] = cart.id
    return render(request, 'shop/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    request.session['cart_id'] = cart.id
    product = get_object_or_404(Product, id=product_id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('shop:cart')