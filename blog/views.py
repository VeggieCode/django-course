from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

class PostListView(ListView):
    #What model to query
    model = Post
    # When calling ClassView.as_view() this tries to render a template with the next syntax:
    template_name = 'blog/home.html' #default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # Name of the key-value dictionary
    ordering = ['-date_posted'] # - symbol changes the order to descending

class PostDetailView(DetailView):
    #What model to query
    model = Post    

class PostCreateView(LoginRequiredMixin, CreateView):
    #What model to query
    model = Post
    fields = ['title', 'content']
    #default: template_name: <model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user # Current login user asigned to author field on form
        return super().form_valid(form) # This calls get_absolute_url on the model if defined.     
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    #What model to query
    model = Post
    fields = ['title', 'content']
    #default: template_name: <model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user # Current login user asigned to author field on form
        return super().form_valid(form) # This calls get_absolute_url on the model if defined.

    # This method is overriding on UserPassesTestMixin class, which is called to evaluate a condition using the
    # current model on the model form
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            is_authorized = True
        else:
            is_authorized = False
        return is_authorized


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)

# ListViews, DetailViews, CreateViews, UpdateViews, DeleteViews