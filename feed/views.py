from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from followers.models import Follower
from .models import Post


class HomePage(TemplateView):
    http_method_names = ['get']
    template_name = 'feed/homepage.html'
    http_method_names = ['get']

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            following = list(
                Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
            )
            if not following:
                # Show the default 30
                posts = Post.objects.all().order_by('-id')[:30]
            else:
                posts = Post.objects.filter(author__in=following).order_by('-id')[:60]
        else:
            posts = Post.objects.all().order_by('-id')[:30]
        context["posts"] = posts
        return context
        
class PostDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"

class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'feed/create.html'
    fields = ['text',]
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)