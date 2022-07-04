import product as product
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import product, Customer, Category, cart, Appointment, Feedback, Order
from django.db.models import Q
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .helpers import send_forget_password_mail
import razorpay



# Create your views here.


def index(request):
    # to get all categories from category model
    categories = Category.get_all_categories()
    return render(request, 'shop/index.html', {'categories': categories})


def aboutus(request):
    return render(request, 'shop/aboutus.html')


def contact(request):
    return render(request, 'shop/contactus.html')



def bangles(request):
    categories = Category.get_all_categories()
    # to get particular category that user has selected
    categoryID = request.GET.get('category')
    # fetch all products of that category
    products = product.get_all_products_by_category_id(categoryID)

    data = {}
    data['products'] = products
    data['Categoris'] = categories
    return render(request, 'shop/bangles.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'shop/signup.html')
    else:
        # fetch deails to database
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email

        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        # for signup indentation
        if (not first_name):
            error_message = "First name Required !!!"
        elif not last_name:
            error_message = "Last name Required !!!"
        elif not phone:
            error_message = "Phone Required !!!"
        elif len(phone) < 10:
            error_message = "phone no should be equal to 10 digits"
        elif not email:
            error_message = "email Required !!!"
        elif not password:
            error_message = "password Required !!!"
        elif len(password) < 5:
            error_message = "password should be greater than 5"
        elif customer.isExists():
            error_message = "Email Address is already registered"
        # saving
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('ShopHome')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'shop/signup.html', data)





def login(request):
    if request.method == 'GET':
        return render(request, 'shop/login.html')
    else:
        # fetch details to database
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['session_email'] = customer.email

                return redirect('ShopHome')
            else:
                error_message = 'Email or password invalid!!'
        else:
            error_message = 'Email or password invalid!!'

        return render(request, 'shop/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


# @login_required(login_url='/shop/login')
def add_to_cart(request):
    session_email1 = request.session.get('session_email')
    customer = Customer.get_customer_by_email(email=session_email1)
    # print(session_email1)
    # get product id
    product_id = request.GET.get('prod_id')
    # search product by id
    products = product.objects.get(id=product_id)
    #save to cart
    cart(email=customer, product=products).save()
    # return render(request,'shop/cart.html')
    return redirect('show_cart')


def show_cart(request):
    # get customer email from session
    session_email1 = request.session.get('session_email')
    # get customer objects from email that is same as session email
    customers = Customer.objects.get(email=session_email1)
    # get all the objects from cart which is equal to cutomers
    carts = cart.objects.filter(email=customers)
    amount = 0.0
    GST = 0.0
    total_amount = 0.0
    # fetching all cart products by customer
    cart_product = [p for p in cart.objects.all() if p.email == customers]
    if cart_product:
        # calculate all products price with its quantity
        for p in cart_product:
            amount = (p.quantity * p.product.price)
            GST = amount * 3 / 100
            total_amount += amount + GST
        return render(request, 'shop/cart.html',
                      {'carts': carts, 'total_amount': total_amount, 'amount': amount, 'GST': GST})
    else:
        return render(request, 'shop/empty.html')


def plus_cart(request):
    session_email1 = request.session.get('session_email')
    customers = Customer.objects.get(email=session_email1)
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id, customers)
        c = cart.objects.get(Q(product=prod_id) & Q(email=customers))
        c.quantity += 1
        c.save()
        amount = 0.0
        total_amount = 0.0
        GST = 0.0
        cart_product = [p for p in cart.objects.all() if p.email == customers]
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            GST = amount * 3 / 100
            total_amount = amount + GST

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'GST': GST,
            'total_amount': total_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    session_email1 = request.session.get('session_email')
    customers = Customer.objects.get(email=session_email1)
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id, customers)
        c = cart.objects.get(Q(product=prod_id) & Q(email=customers))
        c.quantity -= 1
        c.save()
        amount = 0.0
        total_amount = 0.0
        GST = 0.0
        cart_product = [p for p in cart.objects.all() if p.email == customers]
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            GST = amount * 3 / 100
            total_amount = amount + GST

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'GST': GST,
            'total_amount': total_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    session_email1 = request.session.get('session_email')
    customers = Customer.objects.get(email=session_email1)
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id, customers)
        c = cart.objects.get(Q(product=prod_id) & Q(email=customers))
        c.delete()
        amount = 0.0
        total_amount = 0.0
        GST = 0.0
        cart_product = [p for p in cart.objects.all() if p.email == customers]
        for p in cart_product:
            amount = (p.quantity * p.product.price)
            GST = amount * 3 / 100
            total_amount += amount + GST

        data = {
            'amount': amount,
            'GST': GST,
            'total_amount': total_amount
        }
        return JsonResponse(data)


def get_price(request):
    # get url request
    page = requests.get("https://www.goodreturns.in/gold-rates/#Today+24+Carat+Gold+Rate+Per+Gram+in+India+%28INR%29")
    # covert into html
    soup = BeautifulSoup(page.content, 'html.parser')
    # for specific class
    info = soup.find_all(class_='odd_row')
    count = 0
    for items in info:
        count += 1
        if count == 2:
            item = items.get_text()
            break
    pages = requests.get("https://www.goodreturns.in/gold-rates/#Today+24+Carat+Gold+Rate+Per+Gram+in+India+%28INR%29")
    soups = BeautifulSoup(pages.content, 'html.parser')
    infos = soups.find_all(class_='odd_row')
    cnt = 0
    for gold in infos:
        cnt += 1
        if cnt == 4:
            it = gold.get_text()
            break

    pages = requests.get("https://www.goodreturns.in/silver-rates/")
    so = BeautifulSoup(pages.content, 'html.parser')
    inf = so.find_all(class_='odd_row')
    cntu = 0
    for silver in inf:
        cntu += 1
        if cntu == 2:
            silver = silver.get_text()
            break

    pages = requests.get("https://www.goodreturns.in/platinum-price.html#Indian+Major+Cities+Platinum+Rates+Today")
    so = BeautifulSoup(pages.content, 'html.parser')
    i = so.find_all(class_='odd_row')
    c = 0
    for platinum in i:
        c += 1
        if c == 2:
            platinum = platinum.get_text()
            break

    return render(request, 'shop/price.html', {'item': item, 'it': it , 'silver':silver, 'platinum': platinum})


def view(request):
    session_email1 = request.session.get('session_email')
    customer = Customer.get_customer_by_email(email=session_email1)
    product_id = request.GET.get('product_id')
    print(product_id)
    item_already_in_cart = False
    item_already_in_cart = cart.objects.filter(Q(product=product_id) & Q(email=customer)).exists()
    products = product.objects.get(id=product_id)
    return render(request, 'shop/product.html', {'products': products, 'item_already_in_cart': item_already_in_cart})


def appointment(request):
    if request.method == "GET":
        return render(request, 'shop/appointment.html')
    else:
        appointment = Appointment()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        purpose = request.POST.get('purpose')
        date = request.POST.get('date')

        appointment.name = name
        appointment.email = email
        appointment.phone = phone
        appointment.purpose = purpose
        appointment.date = date
        appointment.save()

        return redirect('ShopHome')


def feedback(request):
    if request.method == "GET":
        return render(request, 'shop/feedback.html')
    else:
        feed = Feedback()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        feedback = request.POST.get('feedback')

        feed.name = name
        feed.email = email
        feed.phone = phone
        feed.feedback = feedback
        feed.save()

        return redirect('ShopHome')


def checkout(request):
    session_email1 = request.session.get('session_email')
    customers = Customer.objects.get(email=session_email1)
    cart_items = cart.objects.filter(email=customers)
    amount = 0.0
    total_amount = 0.0
    GST = 0.0
    cart_product = [p for p in cart.objects.all() if p.email == customers]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            GST = amount * 3 / 100
            total_amount = int(amount + GST)
    if request.method == 'POST':
       razor_amount = int(total_amount) * 100
       print(razor_amount)
       client = razorpay.Client(auth=('rzp_test_OjQsAbYLopmKyW', 'DOYoxn0YrpmFO7kVaMBYFtj8'))
       payment = client.order.create({"amount": razor_amount, "currency": "INR", "payment_capture": "1"})
       print(payment)
       for c in cart_items:
            Order(email=customers, product=c.product, quantity=c.quantity, payment_id=payment['id']).save()

       return render(request,'shop/checkout.html',{'payment':payment})

    return render(request, 'shop/checkout.html', { 'cart_items': cart_items,'total_amount': total_amount})


def paymentdone(request):
    session_email1 = request.session.get('session_email')
    customers = Customer.objects.get(email=session_email1)
    carts = cart.objects.filter(email=customers)
    for c in carts:
        Order(email=customers, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


def orders(request):
    session_email1 = request.session.get('session_email')
    customers = Customer.objects.get(email=session_email1)
    order = Order.objects.filter(email=customers)
    return render(request, 'shop/orders.html', {'order': order})


def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        customer = Customer.get_customer_by_email(email)
        request.session['customer'] = customer.id
        print(customer)

        if not Customer.objects.filter(email=customer).first():
            error_message = "No user found with this email !!!"
            return render(request, 'shop/forgetpassword.html', {'error': error_message})

        user_obj = Customer.objects.get(email=email)
        token = customer
        send_forget_password_mail(user_obj, token)
        error_message = "Email has been sent !!!"
        return render(request, 'shop/forgetpassword.html', {'error': error_message})

    return render(request, 'shop/forgetpassword.html')


def changepassword(request, token):
    profile_obj = Customer.objects.get(email=token)

    if request.method == 'GET':
        return render(request, 'shop/changepassword.html', {'profile_obj': profile_obj})
    else:

        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        if not Customer.objects.filter(email=profile_obj).first():
            error_message = "No user found with this email !!!"
            return render(request, 'shop/changepassword.html', {'error': error_message})
        if newpassword != confirmpassword:
            error_message = "Both should be equal !!!"
            return render(request, 'shop/changepassword.html', {'error': error_message})

        # context = {'user_id':profile_obj.Customer.first_name}
        user_obj = Customer.objects.get(email=profile_obj)

        # user_obj = Customer.objects.get(email=email)
        #     customer.password = make_password(customer.password)

        user_obj.password = newpassword
        user_obj.password = make_password(user_obj.password)
        user_obj.save()
        request.session.clear()
        return redirect('login')
