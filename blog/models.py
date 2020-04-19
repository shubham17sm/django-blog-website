from django.db import models
from django.contrib.auth import get_user_model
from tinymce import HTMLField
from django.urls import reverse 
from django.db.models.signals import pre_save
from myproject.utils import unique_slug_generator

# Create your models here.

User = get_user_model()

class PostPerView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username 


class Category(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post-by-category', kwargs={
            'slug': self.slug
        })


    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('BlogPost', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


STATUS_CHOICES = ( 
   ('draft', 'Draft'), 
   ('published', 'Published'), 
) 


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField(default='write blog content')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    bestarticle = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    status = models.CharField(max_length = 35, choices = STATUS_CHOICES, 
                                                      default ='draft') 
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-view', kwargs={
            'slug': self.slug
        })


    def total_likes(self):
        return self.likes.count()


    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


    @property
    def view_count(self):
        return PostPerView.objects.filter(post=self).count()

        

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=BlogPost)