from itertools import product
from lib2to3.fixes.fix_input import context

from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Category, Cart, CartProduct
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm


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

    cart_items = []
    for item in cart.cartproduct_set.all():
        total_price_per_item = item.product.price * item.quantity
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': total_price_per_item
        })

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'shop/cart.html', context)

def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    request.session['cart_id'] = cart.id
    product = get_object_or_404(Product, id=product_id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('shop:cart')

def remove_from_cart(request, product_id):
    cart,_ = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_product = CartProduct.objects.get(cart=cart, product=product)
        cart_product.delete()
    except CartProduct.DoesNotExist:
        pass

    return redirect('shop:cart')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    review_form = ReviewForm()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('shop:product_detail', product_id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form
    }

    return render(request, 'shop/product_detail.html', context)