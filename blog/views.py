from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import CommentForm


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
