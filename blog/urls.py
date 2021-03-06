from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.API.resources import PostViewSet, UserViewSet
from blog.views import UserLogin, UserLogout, Register, MainPage, \
    PostDetailView, PostListView, CategoryDetailView, TagDetailView, \
    AuthorDetailView, Contact, CommentCreateView


router = DefaultRouter()
router.register(r'post_api', PostViewSet)
router.register(r'user_api', UserViewSet)


urlpatterns = [
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
    path('', MainPage.as_view(), name='index'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(),
         name='category_details'),
    path('tag/<slug:slug>/', TagDetailView.as_view(),
         name='tag_details'),
    path('contact/', Contact.as_view(), name='contact'),
    path('', include(router.urls)),
    path('author/<slug:slug>/', AuthorDetailView.as_view(),
         name='author'),
    path('comment/', CommentCreateView.as_view(), name="comment"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),


]
