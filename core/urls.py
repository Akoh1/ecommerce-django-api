from django.urls import path

from .views import auth, cart

urlpatterns = [
    path('', auth.index, name='index'),
    path('register', auth.RegisterView.as_view(), name="register"),
    path('login', auth.LoginView.as_view(), name="login"),
    path('user', auth.UserView.as_view(), name="user"),
    path('billing-address', auth.BillingAddressView.as_view(), name="billing-address"),
    path('states', auth.StateList.as_view(), name="states"),
    path('countries', auth.CountryList.as_view(), name="countries"),
    path('logout', auth.LogoutView.as_view(), name="logout"),
    path('products', cart.ProductList.as_view(), name="products"),
    path('order/items', cart.OrderItemsView.as_view(), name="order-items"),
    path('cart', cart.CartView.as_view(), name="add-to-cart")
    # path('comments/', comments.CommentListView.as_view()),
    # path('comments/<int:pk>', comments.CommentDetailView.as_view()),
]