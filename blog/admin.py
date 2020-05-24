from django.contrib import admin

from .models import BlogPost, Author, Category, Subscribe, Tags, Comment, PostPerView, Bookmark, BookmarkPost
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Subscribe)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(PostPerView)
admin.site.register(Bookmark)
admin.site.register(BookmarkPost)