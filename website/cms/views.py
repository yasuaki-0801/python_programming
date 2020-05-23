from django.shortcuts import render
from .models import Post,Tag,Category,Comment, Reply
from django.views import generic
from django.db.models import Count, Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from cms.forms import CommentForm, ReplyForm,ContactForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _



# Create your views here.
def index_template(request):
    return render(request, 'index.html')

def aboutme(request):
    return render(request, 'cms/aboutme.html')
    

class PostDetailView(DetailView):
    """公開記事の一覧を表示する。"""
    model = Post
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj



class IndexView(ListView):

    model = Post
    template_name = 'cms/index.html'
    paginate_by = 3


class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))

class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True))
    )

class CategoryPostView(ListView):
    model = Post
    template_name = 'cms/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TagPostView(ListView):
    model = Post
    template_name = 'cms/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class SearchPostView(ListView):
    model = Post
    template_name = 'cms/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('cms:post_detail', pk=post_pk)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context

@login_required
def comment_approve(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('cms:post_detail', pk=comment.post.pk)
 
 
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('cms:post_detail', pk=comment.post.pk)

class ReplyFormView(CreateView):
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('cms:post_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    return redirect('cms:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('cms:post_detail', pk=reply.comment.post.pk)

class ContactFormView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('cms:contact_result')#追加箇所

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'contact/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = _("お問い合わせは正常に送信されました。")
        return context

