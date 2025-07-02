from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from followers.models import Follower
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUpdateForm, AvatarUpdateForm, CustomPasswordChangeForm
from feed.models import Post

class UpdateProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profiles/update_profile.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'form': ProfileUpdateForm(instance=request.user),
            'avatar_form': AvatarUpdateForm(instance=request.user.profile),
            'password_form': CustomPasswordChangeForm(user=request.user),
        })

    def post(self, request, *args, **kwargs):
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()

        if avatar_form.is_valid():
            avatar_form.save()

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)

        return redirect("update_profile")
    
class ProfileDetailView(DetailView):
    model = User
    template_name = "profiles/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count()
        return context
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.POST

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        
        try:
            other_user = User.objects.get(username=data['username'])

        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        
        if data['action'] == "follow":

            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user, 
                )
            except Follower.DoesNotExist:
                follower = None
            
            if follower:
                follower.delete()

        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == "follow" else "Follow",
            'followers_count': Follower.objects.filter(following=other_user).count()
        })