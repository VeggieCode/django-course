from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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

# ListViews, DetailViews, CreateViews, UpdateViews, DeleteViews
class PostListView(ListView):
    #What model to query in order to create the list
    model = Post
    
    # When calling ClassView.as_view() this tries to render a template with the next syntax:
    # On this case we are changing the default template to render blog/home.html
    template_name = 'blog/home.html' #default: <app>/<model>_<viewtype>.html

    #By default ClassListView sets the dictionary context with the key "object_list" containing the
    #post list.
    #In order to change this behaviour we can customise the name overriding the next propertie:
    context_object_name = 'posts' # Name of the key-value dictionary

    #Also we can determine the order and attribute of the list:
    # Symbol: - Descending order
    # Symbol: + Ascending order
    ordering = ['-date_posted'] # - symbol changes the order to descending  "

    #It is not neccesary import paginator module
    paginate_by = 5

class UserPostListView(ListView):    
    model = Post        
    template_name = 'blog/user_posts.html' #default: <app>/<model>_<viewtype>.html    
    context_object_name = 'posts' # Name of the key-value dictionary

    #Since we are overriding the QuerySet from the parent, we are ignoring de OrderBy from before
    # ordering = ['-date_posted']

    #It is not neccesary import paginator module
    paginate_by = 5

    # In order to modify the queryset from this list view
    def get_queryset(self):
        #if dont exist that user we are show 404
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        #Since we are overriding the QuerySet from the parent, we are ignoring de OrderBy written above
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    # DetailView search by default for the template name with the next convention:
    # <app>/<model>_detail.html
    # template_name = blog/post_detail.html

    #What model to query
    model = Post

    #context name of the model by default is 'object'
    # context_object_name = 'object'

class PostCreateView(LoginRequiredMixin, CreateView):
    #What model to query
    model = Post
    
    #Fields to be modified by the view
    fields = ['title', 'content']
    
    #default: template_name: <model>_form.html

    def form_valid(self, form):
        # We need add the author of the post before saving it to the database
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
        return self.is_owner()
    
    def is_owner(self):
        post = self.get_object()
        return self.request.user == post.author            

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    #What model to affect
    model = Post

    # Where to redirect the user when confirm deletion and this succed
    success_url = reverse_lazy('blog-home')
    #Template name for delete view by default follows the next convention:
    # <model>_confirm_delete.html
    # template_name = "post_confirm_delete.html"

    # This method is overriding on UserPassesTestMixin class, which is called to evaluate a condition using the
    # current model on the model form
    def test_func(self):        
        return self.is_owner()
    
    def is_owner(self):
        post = self.get_object()
        return self.request.user == post.author

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)