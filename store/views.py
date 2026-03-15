from django.shortcuts import render
from django.conf import settings
from .models import Fruit, Order
import razorpay
from django.http import HttpResponse

# HOME PAGE
def home(request):

    fruits = Fruit.objects.all()

    return render(request, "home.html", {
        "fruits": fruits
    })

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
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



def payment_success(request):

    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    name = request.POST.get("name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    total = request.POST.get("total")

    params_dict = {
        "razorpay_order_id": order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)

        Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            total_amount=total,
            payment_method="Online",
            payment_status="Paid"
        )

        return redirect(f"/order-success/?name={name}&phone={phone}&address={address}&total={total}")

    except:
        return HttpResponse("Payment verification failed")