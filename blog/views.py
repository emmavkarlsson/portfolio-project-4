from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 12


class FeaturedPost(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(slug=slug)
        comments = post.comments.order_by('created-on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "featured_post.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            }
        )
