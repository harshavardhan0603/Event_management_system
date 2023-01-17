from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import date as datee
import razorpay
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import *

def home(request):
    # v = venue(venue_name= "venue1", capacity = 1500 , charges = 40000 , image = "1.png")
    # v.save()
    # v = venue(venue_name= "venue2", capacity = 2000, charges = 50000 , image = "2.png")
    # v.save()
    # v = venue(venue_name= "venue3", capacity = 1700 , charges = 45000 , image = "3.png")
    # v.save()
    # v = venue(venue_name= "venue4", capacity = 3000 , charges = 100000 , image = "4.png")
    # v.save()
    # v = venue(venue_name= "venue5", capacity = 2500 , charges = 75000 , image = "5.png")
    # v.save()
    return render(request,"home.html")

def index(request):
    if request.user.is_authenticated:
        return render(request,"main.html")
    else:
        return render(request,"home.html")

def registerpage(request):
    if request.method=='POST':
        username=request.POST['username']
        if User.objects.filter(username= username).exists():
            messages.info(request,"username already exists")
            return redirect('signup')
        password=request.POST['password1']
        confirm_password=request.POST['password2']
        if password==confirm_password:
            user = User.objects.create_user(username=username,password=password)
            user.save()
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,"passwords are not matching")
            return redirect('signup')
    else:
         return render(request,"signup.html")

def log_in(request):

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,"user doesn't exits or password wrong")
            return redirect("login")
    return render(request, "login.html")

def log_out(request):
    logout(request)
    return redirect("home")

def contact(request):
    return render(request, "contactus.html")

def book(request):  
    venues = venue.objects.all()

    if request.user.is_authenticated:
        if request.method == 'POST':
            if  booking_data.objects.filter(date =request.POST["date"]).filter(venue_name = request.POST["venue"]).exists():
                messages.info(request,request.POST["venue"] + "is already booked for the date: " +request.POST["date"] +" please choose other dates")
                return redirect("book")

            vv = venue.objects.get(venue_name = request.POST["venue"])
            if vv.capacity  < int(request.POST["guest"]):
                messages.info(request,"guests are more than venue capacity ")
                return redirect("book")
            table = []
            value = { '0' : "Not Required",'1' : "Normal", '2' : "Delux",'3' : "Royal"}


            data = booking_data(  user = request.user,
                                    venue_name = request.POST["venue"],
                                    EventType = request.POST["event"],
                                    date = request.POST["date"],
                                    breakfast = request.POST["breakfast"],
                                    lunch = request.POST["lunch"],
                                    TeaSnacks = request.POST["Tea and Snacks"],
                                    dinner = request.POST["dinner"],
                                    Nonveg = request.POST["Nonveg"],
                                    NoofGuest = request.POST["guest"],
                                    Decoration = request.POST["decoration"] )

            v =  venue.objects.all().filter(venue_name = data.venue_name)
            v = v[0]
            table.append({"a":"Breakfast", "b":value[data.breakfast],"c":(int(data.breakfast))*100 ,"d":(int(data.breakfast))*100*int(data.NoofGuest) })
            table.append({"a":"Lunch", "b":value[data.lunch],"c":(int(data.lunch))*175 ,"d":(int(data.lunch))*175*int(data.NoofGuest) })
            table.append({"a":"Dinner", "b":value[data.dinner],"c":(int(data.dinner))*200 ,"d":(int(data.dinner))*200*int(data.NoofGuest) })
            table.append({"a":"Decoration", "b":value[data.Decoration],"c":(int(data.Decoration))*15000 ,"d":(int(data.Decoration))*15000})
            



            # amount calculation
            amt = 0

            amt += ((int(data.breakfast))*100 + (int(data.lunch))*175 + (int(data.dinner))*200 ) * int(data.NoofGuest)
            amt += int(data.Decoration)*15000
            amt += (int(v.charges))
            data.Amount = amt
            data.save()

            #generating pdf reciept
            template_path = 'reciept.html'


            response = HttpResponse(content_type='application/pdf')

            response['Content-Disposition'] = 'filename="reciept.pdf"'

            template = get_template(template_path)

            html = template.render({"data":data, "table": table , "venue": v })

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)

             # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
            

        return render(request,"book.html", {"venues":venues} )

    return render(request,"home.html")

def history(request):
    if request.user.is_authenticated:
        today = datee.today()
        all = booking_data.objects.all().filter(user=request.user)
        hist = []
        prev = []
        for i in all:
            if i.date > today :
                hist.append(i)
            else:
                prev.append(i)
                
        # status = booking_status.object.all().filter(user=request.user)
        return render(request,"history.html", {"hist":hist ,"prev":prev})
    else:
        return render(request,"home.html")

def view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            venues = venue.objects.filter(venue_name__contains = request.POST['input'])
            if len(venues) != 0:
                return render(request,"view.html", {"venues":venues})

        venues = venue.objects.all()
        return render(request,"view.html", {"venues":venues})
    
    else:
        return render(request,"home.html")

def update(request, n):
    task = booking_data.objects.get(id = n)
    forms = booking_form(instance=task)
    if request.method == "POST":
        form = booking_form(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("/")
    return render(request,"update.html",{"forms":forms })

def delete(request, n):
    task = booking_data.objects.get(id = n)
    task.delete()
    return redirect('/history')

def feedback(request, n):
    if booking_review.objects.filter(booking_id = n).exists():
        review = booking_review.objects.get(booking_id = n)
        if request.method == "POST":
            review.rating = request.POST['rating']
            review.comment = request.POST['comment']   
            review.save()        
            return redirect("/review") 
        return render(request, "feedback.html", {"edit":True, "rating":review.rating, "comment": review.comment})
    else:
        if request.method == "POST":
        
            task = booking_review()
            task.user = request.user
            task.booking = booking_data.objects.get(id = n)
            task.rating = request.POST['rating']
            task.comment = request.POST['comment']           
            task.save()
            return redirect("/review")  
    return render(request,"feedback.html" , {"edit":True})


def receipt(request, n):
    data = booking_data.objects.get(id = n)
    v =  venue.objects.all().filter(venue_name = data.venue_name)
    v = v[0]
    value = { '0' : "Not Required",'1' : "Normal", '2' : "Delux",'3' : "Royal"}
    table = []
    table.append({"a":"Breakfast", "b":value[str(data.breakfast)],"c":(int(data.breakfast))*100 ,"d":(int(data.breakfast))*100*int(data.NoofGuest) })
    table.append({"a":"Lunch", "b":value[str(data.lunch)],"c":(int(data.lunch))*175 ,"d":(int(data.lunch))*175*int(data.NoofGuest) })
    table.append({"a":"Dinner", "b":value[str(data.dinner)],"c":(int(data.dinner))*200 ,"d":(int(data.dinner))*200*int(data.NoofGuest) })
    table.append({"a":"Decoration", "b":value[str(data.Decoration)],"c":(int(data.Decoration))*15000 ,"d":(int(data.Decoration))*15000})


            # amount calculation
    amt = 0

    amt += ((int(data.breakfast))*100 + (int(data.lunch))*175 + (int(data.dinner))*200 ) * int(data.NoofGuest)
    amt += int(data.Decoration)*15000
    amt += (int(v.charges))
    data.Amount = amt
    data.save()

            #generating pdf reciept
    template_path = 'reciept.html'


    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="reciept.pdf"'

    template = get_template(template_path)

    html = template.render({"data":data, "table": table , "venue": v })

            # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

             # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
            



def review(request):
    if request.user.is_authenticated:
        present = datee.today()
        prev = booking_data.objects.all().filter(user=request.user)
        data = []
        for i in prev  :
            if i.date < present :
                data.append(i)

        return render(request,"review.html", { "data":data })
    
    else:
        return render(request,"home.html")




# def order_payment(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         amount = request.POST.get("amount")
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         razorpay_order = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#         order = Order.objects.create(
#             name=name, amount=amount, provider_order_id= "id"
#         )
#         order.save()
#         return render(
#             request,
#             "payment.html",
#             {
#                 "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
#                 "razorpay_key":123198413132,
#                 "order": order,
#             },
#         )
#     return render(request, "payment.html")


    


# def pdf_report_create(request):

#     template_path = 'details.html'


#     response = HttpResponse(content_type='application/pdf')

#     response['Content-Disposition'] = 'filename="reciept.pdf"'

#     template = get_template(template_path)

#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response)
#     # if error then show some funy view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response


    

