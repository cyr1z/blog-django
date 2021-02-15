from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.postgres.search import SearchVector, SearchQuery, \
    SearchRank
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView, ListView, TemplateView, \
    DetailView, FormView

from blog.forms import SignUpForm, CreateCommentForm, ContactForm
from blog.models import Post, Category, Tag, BlogUser, Comment, AlbumImage, \
    SiteSettings
from blog_with_rest.settings import DEFAULT_POST_IMAGE, EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD


class UserLogin(LoginView, ):
    """ login """
    template_name = 'login.html'


class Register(CreateView, ):
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


class PostListView(ListView):
    """
    List of posts
    """
    model = Post
    paginate_by = 5
    template_name = 'all_posts.html'
    queryset = Post.objects.filter(is_published=True)
    context_object_name = 'posts_list'

    def get_queryset(self):
        search_query = self.request.GET.get('q')

        if search_query:
            search_query = SearchQuery(search_query)
            search_vector = SearchVector('title', 'text')
            return Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

        return self.queryset


class PostDetailView(DetailView):
    """
    Post detail
    """
    model = Post
    template_name = 'blog-single.html'

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.increment_view_count()
        return item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add comment_form
        comment_form = CreateCommentForm(self.request.POST or None)
        comment_form.fields['text'].widget.attrs.update(
            {'class': 'form-control'})
        context.update({'add_comment_form': comment_form})
        # add comments_count
        context.update({'comments_count': self.object.post_comments.count()})
        # add similar posts
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(
            tags__in=post_tags_ids
        ).exclude(id=self.object.id)
        similar_posts = similar_posts.annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-published_at')[:2]
        context.update({'similar_posts': similar_posts})
        context.update({'default_image': DEFAULT_POST_IMAGE})
        # add gallery images
        try:
            images = AlbumImage.objects.filter(album=self.object.album)
            context.update({'images': images})
        except:
            context.update({'images': None})
        return context


class CategoryDetailView(DetailView):
    """
    List of category posts
    """
    model = Category
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add posts pagination
        all_posts = self.get_object().category_posts.filter(is_published=True)
        paginator = Paginator(all_posts, 5)
        page = self.request.GET.get('page', 1)
        posts = paginator.get_page(page)
        context.update({'posts': posts})
        return context


class TagDetailView(DetailView):
    """
    Tag
    """
    model = Tag
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add posts pagination
        all_posts = self.get_object().tag_posts.all()
        paginator = Paginator(all_posts, 5)
        page = self.request.GET.get('page', 1)
        posts = paginator.get_page(page)
        context.update({'posts': posts})
        return context


class MainPage(TemplateView):
    """
    main page / index page
    """
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # add latest post
        latest_post = Post.objects.order_by('-published_at').filter(is_published=True).first()
        if latest_post:
            context.update({'latest_post': latest_post})
        # add 3 next latest posts
        next_three_posts = Post.objects.filter(is_published=True).order_by('-published_at')[1:4]
        if next_three_posts:
            context.update({'next_three_posts': next_three_posts})
        # add pinned top post
        pinned_on_main_top_post = Post.objects.filter(
            pinned_on_main_top=True).first()
        if pinned_on_main_top_post:
            context.update({
                'pinned_on_main_top_post': pinned_on_main_top_post
            })
        # add pinned bottom post
        pinned_on_main_bottom_post = Post.objects.filter(
            pinned_on_main_bottom=True).first()
        if pinned_on_main_bottom_post:
            context.update(
                {'pinned_on_main_bottom_post': pinned_on_main_bottom_post}
            )

        return context


class Contact(FormView):
    """
    contact page
    """
    template_name = 'contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        phone = form.cleaned_data['phone']
        name = form.cleaned_data['name']
        to_mail = [SiteSettings.objects.first().contact_email, ]

        # try:
        #     send_mail(subject, message, from_email, to_mail)
        # except BadHeaderError:
        #     pass
        messages.success(self.request, 'Your message send.')
        return HttpResponseRedirect(reverse('contact'))


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
