from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post, Profile, Comment
from .forms import CommentForm, PostForm, ProfilePictureForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 12


class FeaturedPost(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "featured_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            }
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "featured_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            }
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('featured_post', args=[slug]))


class AddImage(generic.CreateView):
    form_class = PostForm
    template_name = 'add_image.html'

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class DeletePost(generic.DeleteView):
    """
    Allows users to delete their own posts
    """
    model = Post
    template_name = 'delete_post.html'

    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        return super(DeletePost, self).delete(request, *args, **kwargs)


class EditPost(generic.UpdateView):
    """
    Allows users to update their posts
    """
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class MyPosts(generic.ListView):
    model = Post
    template_name = 'my_posts.html'

    def get_queryset(self):
        return Post.objects.filter(publisher=self.request.user)


class MyLikedPosts(generic.ListView):
    model = Post
    template_name = 'my_likes.html'

    def get_queryset(self):
        return Post.objects.filter(likes=self.request.user)


def profile_view(request):
    """
    Renders the profile page
    """
    if request.method == 'POST':
        profile_form = ProfilePictureForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfilePictureForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form,
    }

    success_url = reverse_lazy('profile')

    return render(request, 'profile.html', context)


def delete_comment(request, comment_id):
    """
    Let's users delete their comments and comments on their own posts
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))