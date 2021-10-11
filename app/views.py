from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Cart, OrderPlaced, Product
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
     def get(self, request):
          totalitem = 0
          mens_wear = Product.objects.filter(category='MW')
          womens_wear = Product.objects.filter(category='WW')
          mobile = Product.objects.filter(category='M')
          watch = Product.objects.filter(category='W')
          food = Product.objects.filter(category='F')
          households = Product.objects.filter(category='HH')
          handwash = Product.objects.filter(category='HW')
          sanitizer = Product.objects.filter(category='S')
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
          return render(request, "app/home.html",{'mens_wear':mens_wear,'womens_wear':womens_wear,'mobile':mobile,'watch':watch,'food':food,'households':households,'handwash':handwash,'sanitizer':sanitizer,'totalitem':totalitem})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
     def get(self, request, pk):
          totalitem = 0
          product = Product.objects.get(pk=pk)
          item_already_in_cart = False
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
               item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
          # print(product)
          return render(request, "app/productdetail.html",{'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
     
     def post(self, request):
          form = CustomerRegistrationForm(request.POST)
          if form.is_valid():
               form.save()
          return render(request, "app/productdetail.html",{'form':form})

@login_required
def add_to_cart(request):
     user = request.user
     product_id = request.GET.get('prod_id')
     print(product_id)
     product = Product.objects.get(id=product_id)
     Cart(user=user,product=product).save()
     return redirect('/cart')

@login_required
def show_cart(request):
     totalitem=0
     if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          user = request.user
          cart = Cart.objects.filter(user=user)
          # print(cart)
          amount = 0.0
          shipping_amount = 70.0
          total_amount = 0.0
          cart_product = [p for p in Cart.objects.all() if p.user==user]
          # print(cart_product)
          if cart_product:
               for p in cart_product:
                    tempamount = (p.quantity * p.product.discounted_price)
                    amount += tempamount
                    total_amount = amount + shipping_amount
               return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':total_amount,'amount':amount,'totalitem':totalitem})
          else:
               return render(request,'app/emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
     if request.method == 'GET':
          prod_id = request.GET['prod_id']
          # print(prod_id)
          c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.quantity+=1
          c.save()
          amount = 0.0
          shipping_amount = 70.0
          cart_product = [p for p in Cart.objects.all() if p.user == request.user]
          for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount

          data = {
               'quantity': c.quantity,
               'amount': amount,
               'totalamount': amount + shipping_amount
               }
          return JsonResponse(data)


def minus_cart(request):
     if request.method == 'GET':
          prod_id = request.GET['prod_id']
          # print(prod_id)
          c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.quantity-=1
          c.save()
          amount = 0.0
          shipping_amount = 70.0
          cart_product = [p for p in Cart.objects.all() if p.user == request.user]
          for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount

          data = {
               'quantity': c.quantity,
               'amount': amount,
               'totalamount': amount + shipping_amount
               }
          return JsonResponse(data)

@login_required
def remove_cart(request):
     if request.method == 'GET':
          prod_id = request.GET['prod_id']
          # print(prod_id)
          c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.delete()
          amount = 0.0
          shipping_amount = 70.0
          cart_product = [p for p in Cart.objects.all() if p.user == request.user]
          for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount

          data = {
               'amount': amount,
               'totalamount': amount + shipping_amount
               }
          return JsonResponse(data)

@login_required
def buy_now(request):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     return render(request, 'app/buynow.html',{'totalitem':totalitem})

def profile(request):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     return render(request, 'app/profile.html',{'totalitem':totalitem})

@login_required
def address(request):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     add = Customer.objects.filter(user=request.user)
     return render(request, 'app/address.html',{'add':add, 'active':'btn-info','totalitem':totalitem})

@login_required
def orders(request):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     op = OrderPlaced.objects.filter(user=request.user)
     return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

def mens_wear(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          mens_wear = Product.objects.filter(category='MW')
     elif data == 'Lee' or data == 'HandM':
          mens_wear = Product.objects.filter(category='MW').filter(brand=data)
     elif data == 'below':
          mens_wear = Product.objects.filter(category='MW').filter(discounted_price__lt=1000)
     elif data == 'above':
          mens_wear = Product.objects.filter(category='MW').filter(discounted_price__gt=1000)
     return render(request, 'app/mens_wear.html',{'mens_wear':mens_wear,'totalitem':totalitem})

def womens_wear(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          womens_wear = Product.objects.filter(category='WW')
     elif data == 'Zara' or data == 'HandM':
          womens_wear = Product.objects.filter(category='WW').filter(brand=data)
     elif data == 'below':
          womens_wear = Product.objects.filter(category='WW').filter(discounted_price__lt=500)
     elif data == 'above':
          womens_wear = Product.objects.filter(category='WW').filter(discounted_price__gt=500)
     return render(request, 'app/womens_wear.html',{'womens_wear':womens_wear,'totalitem':totalitem})

def mobile(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          mobiles = Product.objects.filter(category='M')
     elif data == 'Redmi' or data == 'Oneplus':
          mobiles = Product.objects.filter(category='M').filter(brand=data)
     elif data == 'below':
          mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=15000)
     elif data == 'above':
          mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=15000)
     return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def watch(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          watches = Product.objects.filter(category='W')
     elif data == 'Samsung' or data == 'Boot':
          watches = Product.objects.filter(category='W').filter(brand=data)
     elif data == 'below':
          watches = Product.objects.filter(category='W').filter(discounted_price__lt=4000)
     elif data == 'above':
          watches = Product.objects.filter(category='W').filter(discounted_price__gt=4000)
     return render(request, 'app/watch.html',{'watches':watches,'totalitem':totalitem})

def food(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          food = Product.objects.filter(category='F')
     elif data == 'below':
          food = Product.objects.filter(category='F').filter(discounted_price__lt=280)
     elif data == 'above':
          food = Product.objects.filter(category='F').filter(discounted_price__gt=280)
     return render(request, 'app/food.html',{'food':food,'totalitem':totalitem})

def households(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          households = Product.objects.filter(category='H')
     elif data == 'below':
          households = Product.objects.filter(category='H').filter(discounted_price__lt=75)
     elif data == 'above':
          households = Product.objects.filter(category='H').filter(discounted_price__gt=75)
     return render(request, 'app/households.html',{'households':households,'totalitem':totalitem})

def handwash(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          handwash = Product.objects.filter(category='HW')
     elif data == 'below':
          handwash = Product.objects.filter(category='HW').filter(discounted_price__lt=350)
     elif data == 'above':
          handwash = Product.objects.filter(category='HW').filter(discounted_price__gt=350)
     return render(request, 'app/handwash.html',{'handwash':handwash,'totalitem':totalitem})

def sanitizer(request, data=None):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     if data == None:
          sanitizer = Product.objects.filter(category='S')
     elif data == 'below':
          sanitizer = Product.objects.filter(category='S').filter(discounted_price__lt=110)
     elif data == 'above':
          sanitizer = Product.objects.filter(category='S').filter(discounted_price__gt=110)
     return render(request, 'app/sanitizer.html',{'sanitizer':sanitizer,'totalitem':totalitem})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
     def get(self, request):
          form = CustomerRegistrationForm()
          return render(request, 'app/customerregistration.html',{'form':form})
     def post(self, request):
          form = CustomerRegistrationForm(request.POST)
          if form.is_valid():
               messages.success(request, 'Congratulations!! Registered Successfully')
               form.save()
          return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
     totalitem=0
     if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
     user = request.user
     add = Customer.objects.filter(user=user)
     cart_items = Cart.objects.filter(user=user)
     amount = 0.0
     shipping_amount = 70.0
     totalamount = 0.0
     cart_product = [p for p in Cart.objects.all() if p.user == request.user]
     if cart_product:
          for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
          totalamount = amount + shipping_amount
     return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
     user = request.user
     custid = request.GET.get('custid')
     customer = Customer.objects.get(id=custid)
     cart = Cart.objects.filter(user=user)
     for c in cart:
          OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
          c.delete()
     return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
     def get(self, request):
          totalitem=0
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
               form = CustomerProfileForm()
          return render(request, 'app/profile.html',{'form':form, 'active':'btn-info','totalitem':totalitem})
     def post(self, request):
          form = CustomerProfileForm(request.POST)
          if form.is_valid():
               usr = request.user  #for current user
               name = form.cleaned_data['name']
               locality = form.cleaned_data['locality']
               city = form.cleaned_data['city']
               state = form.cleaned_data['state']
               zipcode = form.cleaned_data['zipcode']
               reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
               reg.save()
               return redirect('address')
               # messages.success(request, 'Congratulations!! Profile Updated Successfully.')
          return render(request, 'app/profile.html',{'form':form})

class SearchResultView(View):
     model = Product
     template_name = 'search_results.html'

     def get_queryset(self): # new
          query = self.request.GET.get('q')
          object_list = Product.objects.filter(
               Q(title__icontains=query)
          )
          return object_list