from taggit.models import Tag
from .models import Post, Comment
from django.db.models import Count
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tag__in=[tag])

    paginator = Paginator(object_list, 5) # 5 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'page': page, 'posts': posts, 'tag': tag}
    return render(request, 'recipes/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tag.values_list('id', flat=True)
    similar_posts = Post.published.filter(tag__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags','-publish')[:5]

    context = {
        'post': post, 
        'comments': comments, 
        'new_comment': new_comment, 
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(request, 'recipes/post/detail.html', context)


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"""
                Read {post.title} at {post_url} 
                \n
                {cd['name']}\'s comments: {cd['comments']}
            """
            send_mail(subject, message, 'thecodexgrey@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'recipes/post/share.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        # getting search query from form
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)

    context = {'form': form, 'query': query, 'results': results}
    return render(request, 'recipes/post/search.html', context)

