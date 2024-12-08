from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem, Coupon
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm


def home(request):
    return render(request, 'shop/home.html')


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'shop/product_list.html', context)


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'shop/category_products.html', {'products': products, 'category': category})


def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)

    cart_items = []
    for item in cart.items.all():
        total_price_per_item = item.subtotal()
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
    cart, _ = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    cart.total_price = cart.total()
    cart.save()

    return redirect('shop:cart')



def remove_from_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass


    cart.total_price = cart.total()
    cart.save()

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


def apply_coupon(request):
    cart = Cart.objects.get(user=request.user)
    coupon_code = request.POST.get('coupon_code')

    try:
        coupon = Coupon.objects.get(code=coupon_code)
        cart.apply_discount(coupon)
        return redirect('shop:cart')
    except Coupon.DoesNotExist:

        return redirect('shop:cart')
