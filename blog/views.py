from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, TemplateView, \
    DetailView, FormView

from blog.forms import SignUpForm, CreateCommentForm
from blog.models import Post, Category, Tag, BlogUser, Comment


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


class AuthorDetailView(DetailView):
    model = BlogUser
    template_name = 'author.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add categories for main menu
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # add popular posts for right column
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        return context


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
        # add categories for main menu
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # add popular posts for right column
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
        # add categories for main menu
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # add popular posts for right column
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        # add comment_form
        comment_form = CreateCommentForm(self.request.POST or None)
        comment_form.fields['text'].widget.attrs.update(
            {'class': 'form-control'})
        context.update({'add_comment_form': comment_form})
        # add comments_count
        context.update({'comments_count': self.object.post_comments.count()})
        return context


class CategoryDetailView(DetailView):
    """
    List of products
        """
    model = Category
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add categories for main menu
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # add popular posts for right column
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        # add posts pagination
        all_posts = self.get_object().category_posts.all()
        paginator = Paginator(all_posts, 5)
        page = self.request.GET.get('page', 1)
        posts = paginator.get_page(page)
        context.update({'posts': posts})
        return context


class TagDetailView(DetailView):
    """
    List of products
        """
    model = Tag
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add categories for main menu
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # add popular posts for right column
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        # add posts pagination
        all_posts = self.get_object().tag_posts.all()
        paginator = Paginator(all_posts, 5)
        page = self.request.GET.get('page', 1)
        posts = paginator.get_page(page)
        context.update({'posts': posts})
        return context


class MainPage(TemplateView):
    """
    main page
    """
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add categories for main menu
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # add latest post
        latest_post = Post.objects.order_by('-published_at').first()
        context.update({'latest_post': latest_post})
        # add 3 next latest posts
        next_three_posts = Post.objects.all().order_by('-published_at')[1:4]
        context.update({'next_three_posts': next_three_posts})
        # add popular posts for right column
        most_popular_posts = Post.objects.all().order_by('-views')[0:5]
        context.update({'most_popular_posts': most_popular_posts})
        # add pinned top post
        pinned_on_main_top_post = Post.objects.filter(
            pinned_on_main_top=True).first()
        context.update({'pinned_on_main_top_post': pinned_on_main_top_post})
        # add pinned bottom post
        pinned_on_main_bottom_post = Post.objects.filter(
            pinned_on_main_bottom=True).first()
        context.update(
            {'pinned_on_main_bottom_post': pinned_on_main_bottom_post})

        return context


class Contact(TemplateView):
    """
     main page
     """
    template_name = 'contact.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add categories for main menu and form
        categories = {_.title: _.slug for _ in Category.objects.all()}
        context.update({'categories': categories})
        # context.update({'form': EmailForm})

        return context

    # def post(self):
    #     form = EmailForm(self.request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         msg = EmailMessage()
    #     messages.success(self.request, 'Your message sent')
    #     return HttpResponseRedirect(reverse('contact'))


@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    """
    Create comment
    """
    form_class = CreateCommentForm
    model = Comment

    def form_valid(self, form):
        comment = form.save(commit=False)
        slug = self.request.POST.get('slug')
        post = Post.objects.get(slug=slug)
        comment.post = post
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form=form)

    def get_success_url(self):
        slug = self.request.POST.get('slug')
        return reverse('post_details', kwargs={'slug': slug})
