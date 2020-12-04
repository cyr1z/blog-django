from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, DetailView

from blog.forms import SignUpForm
from blog.models import Post, Category


class UserLogin(LoginView):
    """ login """
    template_name = 'login.html'


class Register(CreateView):
    """ Sign UP """
    form_class = SignUpForm
    success_url = "/login/"
    template_name = "register.html"


class UserLogout(LoginRequiredMixin, LogoutView):
    """ Logout """
    next_page = '/'
    redirect_field_name = 'next'


class PostListView(ListView):
    """
    List of posts
    """
    model = Post
    paginate_by = 5
    template_name = 'all_posts.html'
    queryset = Post.objects.all()
    context_object_name = 'posts_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        return context


class PostDetailView(DetailView):
    """
    List of products
        """
    model = Post
    template_name = 'blog-single.html'

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.increment_view_count()
        return item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        return context


class CategoryDetailView(DetailView):
    """
    List of products
        """
    model = Category
    template_name = 'categories.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data()
    #     posts = object.
    #     context.update({'category_posts': posts})
    #     return context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        return context


class MainPage(TemplateView):
    """
    main page
    """
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        latest_post = Post.objects.order_by('-published_at').first()
        context.update({'latest_post': latest_post})
        next_three_posts = Post.objects.all().order_by('-published_at')[1:4]
        context.update({'next_three_posts': next_three_posts})
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        pinned_on_main_top_post = Post.objects.filter(
            pinned_on_main_top=True).first()
        context.update({'pinned_on_main_top_post': pinned_on_main_top_post})
        pinned_on_main_bottom_post = Post.objects.filter(
            pinned_on_main_bottom=True).first()
        context.update({'pinned_on_main_bottom_post': pinned_on_main_bottom_post})

        return context



