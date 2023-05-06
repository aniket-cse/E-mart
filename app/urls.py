from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm,MyPasswordResetForm
# from  django.contrib.auth.views import LoginView
urlpatterns = [
    #this is function based views
    # path('', views.home),

    #This is class based views
    path('',views.ProductView.as_view(),name='home'),
    path('search/',views.search,name='search'),

    # path('product-detail/', views.product_detail, name='product-detail'),
    #This is class based views --> yaha 1 ,2 kar ke id ayega
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/',views.remove_cart),


    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('laptop/', views.laptop, name='laptop'),


    


    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    # path('registration/', views.customerregistration, name='customerregistration'),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(
    template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),


    # ---------------Original url-----
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html'),name='login'),
    # path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    # ---------- original url end-----


    #-----------------------------------------------------
    path('register' , views.register_attempt , name="register_attempt"),
    # path('accounts/login/' , views.login_attempt , name="login_attempt"),
    path('token' , views.token_send , name="token_send"),
    path('success' , views.success , name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),
    #----------------------------------------------------




    #payment success full
    path('checkout/', views.checkout, name='checkout'),
    # path('payment-completed/', views.payment_completed_view, name='payment-completed'),
    # path('payment-failed/', views.payment_failed_view, name='payment-failed'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('paypal/',include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
