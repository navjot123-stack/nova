from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import*
# from .models import BillingDetails, CartItem
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
def index(request):
    dd=products.objects.all()
    itm=CartItem.objects.filter(user=request.user).count()
    return render(request, 'index.html',{'dd':dd})

def product_detail(request,id):
    dd=products.objects.get(id=id)
    if request.method=='POST':
        qty=int(request.POST['quantity'])
        x=CartItem(product=dd,quantity=qty,user=request.user)
        x.save()
        return redirect('cart')
    return render(request,'product_details.html',{'d':dd})
def shop(request):
    dd=products.objects.all()
    itm=CartItem.objects.filter(user=request.user).count()
    return render(request, 'shop.html',{'dd':dd})

def cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total_price=sum(item.product.price * item.quantity for item in cart_items)
    return render(request,'cart.html',{'cart_items':cart_items, 'total_price':total_price})


# def add_to_cart(request, product_id):
#     product = get_object_or_404(Addproduct, id=product_id)
#     username = "guest"  # Replace with `request.user.username`
#     cart_item, created = Addcart.objects.get_or_create(product=product, username=username)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('cart')

# def delete_cart_item(request, item_id):
#     cart_item = get_object_or_404(Addcart, id=item_id)
#     cart_item.delete()
#     return redirect('cart')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        lname=request.POST['lname']
        email=request.POST['email']
        message=request.POST['message']
        cnt(name=name,lastname=lname,email=email,message=message).save()
        return HttpResponse("Message sent!")
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

def thankyou(request):
    return render(request, 'thankyou.html')





from django.db.models import Sum, F

# @login_required
def checkout(request):
    if request.method == 'POST':
        # Get form values
        firstname = request.POST.get('c_fname')
        lastname = request.POST.get('c_lname')
        email = request.POST.get('c_email_address')
        phone = request.POST.get('c_phone')
        country = request.POST.get('c_country')
        address = request.POST.get('c_address')
        state = request.POST.get('c_state_country')
        zip_code = request.POST.get('c_postal_zip')
        payment_method = request.POST.get('payment_method')

        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        upi_id = request.POST.get('upi_id')

        # Get all cart items for this user
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('cart')

        # Calculate total
        total_price = cart_items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0

        # Create the Order
        order = Order.objects.create(
            user=request.user,
            firstname=firstname,
            lastname=lastname,
            emailaddress=email,
            phone=phone,
            country=country,
            address=address,
            state=state,
            zip=zip_code,
            payment_method=payment_method,
            card_number=card_number if payment_method == 'online' else None,
            expiry_date=expiry_date if payment_method == 'online' else None,
            cvv=cvv if payment_method == 'online' else None,
            upi_id=upi_id if payment_method == 'upi' else None,
            line_total=total_price
        )

        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                cart_item=item,
                quantity=item.quantity,
                price=item.product.price
            )

        # (Optional) clear the cart
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html')

def about(request):
    return render(request, 'about.html')


def remove(request,id):
    dd=CartItem.objects.get(id=id,user=request.user)
    dd.delete()
    return redirect(cart)


def signup(request):
     if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        # phn=request.POST['phn']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:
            User.objects.create_user(username=name,email=email,password=password).save()
            return redirect(logins)
            # return HttpResponse("done")
        else:
            return HttpResponse("Password should be same")

     return render(request,'signup.html')

def logins(request):
    if request.method=="POST":
        name=request.POST['user']
        password=request.POST['password']
        user=authenticate(username=name,password=password)
        if user:
            login(request,user)
            return redirect(index)
        else:
            return HttpResponse("Invalid credentials")
    return render(request,'login.html')


def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()  # Assuming related_name="items" in OrderItem model

    return render(request, 'order_success.html', {
        'order': order,
        'order_items': order_items
    })