from django.urls import path, include
from . import views
from .api import CartViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='carts')

app_name = 'books'

urlpatterns = [
    path('', views.MyBooksListView.as_view(), name='books_list'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('cart/remove/', views.CartItemRemoveView.as_view(), name='cart_remove'),
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('orders/', views.MyOrdersListView.as_view(), name='my_orders'),
    path('order/complete/<int:order_id>/', views.OrderSuccessView.as_view(), name='order_success'),
    path('order/success-redirect/', views.OrderSuccessRedirectView.as_view(), name='order_success_redirect'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.CustomSignUpView.as_view(), name='signup'),
] 

urlpatterns += router.urls