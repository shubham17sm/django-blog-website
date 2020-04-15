from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from .models import BlogPost, Subscribe, Author, Tags, Category
from .forms import PostForm, CommentForm
from django.contrib import messages

# Create your views here.

def get_author(user):
    queryset = Author.objects.filter(user=user)
    if queryset.exists():
        return queryset[0]
    return None


#search 
def search(request):
    queryset = BlogPost.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search.html', context)


def get_category_count():
    qs = BlogPost.objects.values('categories__title').annotate(Count('categories__title'))
    return qs 


def get_tags_count():
    queryset = BlogPost.objects.values('tags__title').annotate(Count('tags__title'))
    return queryset



#index page view
def index(request):
    # post_list = BlogPost.objects.filter(featured=True)[0:3]
    post_list = BlogPost.objects.filter(bestarticle=True)[0:3]
    latest_post = BlogPost.objects.order_by('-timestamp')[0:3]
    
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Subscribe()
        new_signup.email = email
        new_signup.save()
        messages.info(request, 'Thankyou for subscribing!!')

    context = {
        'post_list': post_list,
        'latest_post': latest_post
    }
    return render(request, "index.html", context)

#blog page view
def blog(request):
    category_count = get_category_count()
    tags_count = get_tags_count()
    latest_sidebar_post = BlogPost.objects.order_by('-timestamp')[0:3]
    latest_blog_post = BlogPost.objects.filter(status='published')
    paginator = Paginator(latest_blog_post, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'latest_blog_post': paginated_queryset,
        'page_request_var': page_request_var,
        'latest_sidebar_post': latest_sidebar_post,
        'category_count': category_count,
        'tags_count': tags_count
    }
    return render(request, "blog.html", context)

#post page view
def post(request, slug):
    category_count = get_category_count()
    tags_count = get_tags_count()
    post = get_object_or_404(BlogPost, slug=slug)
    latest_sidebar_post = BlogPost.objects.order_by('-timestamp')[0:3]

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
          form.instance.user = request.user
          form.instance.post = post
          form.save()
          return redirect(reverse('post-view', kwargs={
              'slug': post.slug
          }))  
    context = {
        'form': form,
        'post': post,
        'latest_sidebar_post': latest_sidebar_post,
        'category_count': category_count,
        'tags_count': tags_count,
    }
    return render(request, "post.html", context)

# create post view
def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-view", kwargs={
                'slug': form.instance.slug
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

# post update view
def post_update(request, slug):
    title = 'Update'
    post = get_object_or_404(BlogPost, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-view", kwargs={
                'slug': form.instance.slug
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

def post_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.delete()
    return redirect(reverse('blog-view'))