from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mens_wear/', views.mens_wear, name='mens_wear'),
    path('mens_wear/<slug:data>', views.mens_wear, name='mens_weardata'),
    path('womens_wear/', views.womens_wear, name='womens_wear'),
    path('womens_wear/<slug:data>', views.womens_wear, name='womens_weardata'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('watch/', views.watch, name='watch'),
    path('watch/<slug:data>', views.watch, name='watchdata'),
    path('food/', views.food, name='food'),
    path('food/<slug:data>', views.food, name='fooddata'),
    path('households/', views.households, name='households'),
    path('households/<slug:data>', views.households, name='householdsdata'),
    path('handwash/', views.handwash, name='handwash'),
    path('handwash/<slug:data>', views.handwash, name='handwashdata'),
    path('sanitizer/', views.sanitizer, name='sanitizer'),
    path('sanitizer/<slug:data>', views.sanitizer, name='sanitizerdata'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    # authentication
    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name="app/passwordchange.html",form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="app/password_reset.html",form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html",form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name='password_reset_complete'),
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
