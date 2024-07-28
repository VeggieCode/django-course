from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
dummy_posts = [
        {
            'author': 'VeggieCode',
            'title': 'Blog Post 1',
            'content': 'Lorem itsum content',
            'date_posted': 'August 27, 2024',
        },
        {
            'author': 'VeggieCode',
            'title': 'Blog Post 2',
            'content': 'Lorem itsum content',
            'date_posted': 'August 28, 2024',
        }
    ]

# Create your views here.
def home(request):    
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)