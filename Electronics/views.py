from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from .models import Laptop, Mobile, About, Cart, Order, Order_Recieve
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum
<<<<<<< HEAD
from django.conf import settings
from django.core.mail import send_mail
=======

MERCHANT_KEY = 'Enter your own Merchant_key'
>>>>>>> 655eeb2307738a1f9148b77752852e5867758949

def home(request):
    electronic = Laptop.objects.all()
    mobile = Mobile.objects.all()
    about = About.objects.all()
    if request.user.is_authenticated:
        my_cart = Cart.objects.all().filter(user_email= request.user.email)
    else:
        my_cart = ""
    return render(request, 'index.html', {"electronic":electronic, "mobile":mobile, "about":about, "cart_item":my_cart})

def detail(request, item, id):
    if(item == "laptop"):
        detail = Laptop.objects.all().filter(slug=id)
    elif (item == "mobile"):
        detail = Mobile.objects.all().filter(slug=id)
    else:
        detail = "none"
    if request.user.is_authenticated:
        my_cart = Cart.objects.all().filter(user_email= request.user.email)
    else:
        my_cart = ""
    return render(request, 'details.html', {"detail":detail, "items":item, "cart_item":my_cart})

def buy(request, item, name):
    if request.method == "GET":
        if(item == "laptop"):
            detail = Laptop.objects.all().filter(slug=name)
        else:
            detail = Mobile.objects.all().filter(slug=name)
        if request.user.is_authenticated:
            my_cart = Cart.objects.all().filter(user_email= request.user.email)
        else:
            my_cart = ""        
        context = {"details":detail,"type":item, "cart_item":my_cart}
        return render(request, "confirm.html",context)

def loginhandle(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        nexturl = request.POST["next"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Login successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return render(request,"")

def signinhandle(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = User.objects._create_user(username, email, password)
        user.save()
        login(request ,user)
        messages.add_message(request, messages.SUCCESS, "Signup successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def add_to_cart(request):
    product_name = request.POST['Product_name']
    price = request.POST['Price']
    temp = Mobile.objects.all().filter(name=product_name)
    if(len(temp) == 0):
        temp = Laptop.objects.all().filter(name=product_name)
        if(len(temp) == 0):
            product_type = "none"
        else:  
            product_type = "laptop"
            details = temp[0]
            cart = Cart.objects.create(product_name=product_name, user_email=request.user.email, price=price, product_type=product_type, Laptop_details = details)
    else:
        details = temp[0]
        product_type = "mobile"
        cart = Cart.objects.create(product_name=product_name, user_email=request.user.email, price=price, product_type=product_type, Mobile_details = details)
    cart.save()
    return HttpResponse(json.dumps({"status": f"{product_name} is added to Cart","product_type":product_type, "product_name":product_name}), content_type="application/json")

def my_cart(request):
    if request.user.is_authenticated:
        cart_list = Cart.objects.all().filter(user_email=request.user.email)
        amount = 0
        for i in range(len(cart_list)):
            amount += int(cart_list[i].price) + 200
        context = {"cart_list":cart_list,"amount":amount}
        return render(request, "my_cart.html", context)
        
@csrf_exempt
def remove(request, id):
    if request.method == "POST":
        cart = Cart.objects.all().filter(id=id)
        cart.delete()
        cart_list = Cart.objects.all().filter(user_email=request.user.email)
        amount = 0
        for i in range(len(cart_list)):
            amount += int(cart_list[i].price)
        print("deleted")
        return HttpResponse(json.dumps({"status": "deleted", "amount":amount}), content_type="application/json")

def order(request):
    product_name = request.POST['Product_Name']
    product_type = request.POST["type"]
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    address1 = request.POST['address1']
    landmark = request.POST['landmark']
    city = request.POST['city']
    state = request.POST['state']
    passcode = request.POST['zip']
    if request.user.is_authenticated:
        user_id = request.user.email
    else:
        user_id = phone
    if product_type == "laptop":
        amount = Laptop.objects.all().filter(name=product_name)[0].price + 200
    if product_type == "mobile":
        amount = Mobile.objects.all().filter(name=product_name)[0].price + 200    
    product_order = Order.objects.create(product_name = product_name, total_amount = amount, order_receive = name,receiver_phone = phone,address = address,address1 = address1,landmark = landmark,city = city,State = state,zip = passcode)
    product_order.save()
    param_dict = {
<<<<<<< HEAD
                'MID': settings.MERCHANT_ID,
=======
                'MID': 'Enter your own MID',
>>>>>>> 655eeb2307738a1f9148b77752852e5867758949
                'ORDER_ID': str(product_order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': user_id,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, settings.MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            pro = Order.objects.get(pk=response_dict['ORDERID'])
            product_name = pro.product_name
            Order_Recieve.objects.create(order_id = response_dict['ORDERID'], product_name = product_name, Currency = response_dict['CURRENCY'], GatewayName = response_dict['GATEWAYNAME'], Respmsg = response_dict['RESPMSG'], Bankname = response_dict['BANKNAME'], PAYMENTMODE = response_dict['PAYMENTMODE'], respcode = response_dict['RESPCODE'], Txnid = response_dict['TXNID'], txnamount = response_dict['TXNAMOUNT'], Status = response_dict['STATUS'], BANKTXNID = response_dict['BANKTXNID'], TXNDATE = response_dict['TXNDATE']).save()
            print('order successful')
            send_mail("Order Confirmation", f"Your order <i>{product_name}</i> has been received. Order No-<i>{response_dict['ORDERID']}</i>\nPlease Contact <b>9650560450</b> for futher updates.", settings.DEFAULT_FROM_EMAIL,["shadman.afzal.7@gmail.com"],fail_silently=True,html_message=True)
            print("mail send")
            messages.add_message(request, messages.SUCCESS, "success")
        else:
            messages.add_message(request, messages.SUCCESS, "failed")
            print('order was not successful because' + response_dict['RESPMSG'])
            Order.objects.get(pk=int(response_dict['ORDERID'])).delete()
    return HttpResponseRedirect("/")

def logoutnhandle(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def my_cart_order(request):
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    address1 = request.POST['address1']
    landmark = request.POST['landmark']
    city = request.POST['city']
    state = request.POST['state']
    passcode = request.POST['zip']
    product_name = []
    amount = 0
    my_cart = Cart.objects.all().filter(user_email = request.user.email)
    for i in range(len(my_cart)):
        product_name.append(my_cart[i].product_name)
        amount = amount + int(my_cart[i].price)+ 200
    user_id = request.user.email
    print(user_id)
    product_order = Order.objects.create(product_name = f"{product_name}",total_amount = amount,order_receive = name,receiver_phone = phone,address = address,address1 = address1,landmark = landmark,city = city,State = state,zip = passcode)
    product_order.save()
    param_dict = {
<<<<<<< HEAD
                'MID': settings.MERCHANT_ID,
=======
                'MID': 'Enter your own MID',
>>>>>>> 655eeb2307738a1f9148b77752852e5867758949
                'ORDER_ID': str(product_order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': user_id,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})