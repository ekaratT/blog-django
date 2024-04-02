from django.shortcuts import render
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count


# Create your views here.


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tag__in=[tag])
    per_page = 1
    paginator = Paginator(posts, per_page=per_page)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    print(tag)
    context = {'page_obj': page_obj, 'tag': tag}
    return render(request, 'core/post_list.html', context)


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 1
#     template_name = 'core/post_list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    # List of active comment for the post
    comments = post.comments.filter(active=True)
    # Form for user to comment
    form = CommentForm()
    # List the similar posts
    post_tags_ids = post.tag.values_list('id', flat=True) #flat=True is passed to get distinct value
    similar_posts = Post.published.filter(tag__in=post_tags_ids).exclude(id=post.id) # Exclude the current post.
    print(f'This is similar posts {similar_posts}')
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-publish')[:4]
    print(f'This is similar posts after annotate {similar_posts}')
    context = {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts}
    return render(request, 'core/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f'Read {post.title} at {post_url}\n\n' \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'core/share.html', context)



def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    form = CommentForm()
    context = {'form': form, 'comment': comment, 'post': post}
    return render(request, 'core/comment.html', context)

