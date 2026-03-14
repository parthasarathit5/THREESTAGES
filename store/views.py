from django.shortcuts import render
from django.conf import settings
from .models import Fruit, Order
import razorpay


# HOME PAGE
def home(request):

    fruits = Fruit.objects.all()

    return render(request, "home.html", {
        "fruits": fruits
    })


# CHECKOUT PAGE
# def checkout(request):

#     if request.method == "POST":

#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         address = request.POST.get("address")
#         payment_method = request.POST.get("payment_method")

#         # temporary total (later connect cart)
#         total = 20


#         # CASH ON DELIVERY
#         if payment_method == "cod":

#             Order.objects.create(
#                 customer_name=name,
#                 phone=phone,
#                 address=address,
#                 total_amount=total,
#                 payment_method="COD",
#                 payment_status="Postpaid"
#             )

#             return render(request, "order_success.html", {
#                 "name": name,
#                 "phone": phone,
#                 "address": address,
#                 "payment": "Cash on Delivery",
#                 "total": total
#             })


#         # ONLINE PAYMENT
#         elif payment_method == "online":

#             Order.objects.create(
#                 customer_name=name,
#                 phone=phone,
#                 address=address,
#                 total_amount=total,
#                 payment_method="Razorpay",
#                 payment_status="Prepaid"
#             )

#             client = razorpay.Client(
#                 auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#             )

#             payment = client.order.create({
#                 "amount": int(total * 100),
#                 "currency": "INR",
#                 "payment_capture": 1
#             })

#             context = {
#                 "payment": payment,
#                 "razorpay_key": settings.RAZORPAY_KEY_ID,
#                 "total": total,
#                 "name": name,
#                 "phone": phone,
#                 "address": address
#             }

#             return render(request, "payment.html", context)

#     return render(request, "checkout.html")


# ORDER SUCCESS PAGE
def order_success(request):

    name = request.GET.get("name")
    phone = request.GET.get("phone")
    address = request.GET.get("address")
    total = request.GET.get("total")

    return render(request, "order_success.html", {
        "name": name,
        "phone": phone,
        "address": address,
        "total": total
    })
def checkout(request):

    # get total safely
    total = request.GET.get("total") or request.POST.get("total") or 0
    total = int(total)

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        # CASH ON DELIVERY
        if payment_method == "cod":

            Order.objects.create(
                customer_name=name,
                phone=phone,
                address=address,
                total_amount=total,
                payment_method="COD",
                payment_status="Postpaid"
            )

            return render(request,"order_success.html",{
                "name":name,
                "phone":phone,
                "address":address,
                "payment":"Cash on Delivery",
                "total":total
            })

        # ONLINE PAYMENT
        elif payment_method == "online":

            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            payment = client.order.create({
                "amount": int(total * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            context = {
                "payment": payment,
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "total": total,
                "name": name,
                "phone": phone,
                "address": address
            }

            return render(request,"payment.html",context)

    return render(request,"checkout.html",{
        "total":total
    })