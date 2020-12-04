from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.API.resources import PostViewSet

router = DefaultRouter()
router.register(r'post_api', PostViewSet)
# router.register(r'purchases_api', PurchaseViewSet)
# router.register(r'product_api', ProductViewSet)
# router.register(r'product_reverse_api', ProductReverseViewSet,
#                 basename='rev_prod')
from blog.views import UserLogin, UserLogout, Register, MainPage, \
    PostDetailView, PostListView, CategoryDetailView, Contact

urlpatterns = [
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
    path('', MainPage.as_view(), name='index'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(),
         name='category_details'),
    path('contact/', Contact.as_view(), name='contact'),
    path('', include(router.urls)),

]
