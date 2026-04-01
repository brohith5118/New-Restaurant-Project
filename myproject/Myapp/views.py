from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Category,Order,OrderItem,FoodItem

# Create your views here.
#login Page
def home(request):
    return render(request,'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)

            # store session
            request.session['username'] = username
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == 'manager':
                return redirect('/manager')
            else:
                return redirect('/menu')

        except User.DoesNotExist:
            return HttpResponse("Invalid credentials")

    return render(request, 'login_view.html')


def logout_view(request):
    request.session.flush()
    return redirect('/')

def is_logged_in(request):
    return request.session.get('user_id')


#Customers Views
def menu(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    userName = request.session.get('username')
    return render(request,'menu.html',{'userName':userName})


def item_details(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'item_details.html')


def user_order(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'user_order.html')


def user_order_history(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'user_order_history.html')


#Managers Views
def manager(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'manager.html')


def current_orders(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'current_orders.html')


def categories(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    
    return render(request,'categories.html')


def food_items(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    return render(request,'food_items.html')


def room_view(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    return render(request,'room_view.html')

def orders_history(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    return render(request,'orders_history.html')