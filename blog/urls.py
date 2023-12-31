from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('my_posts/', views.MyPosts.as_view(), name='my_posts'),
    path('my_likes/', views.MyLikedPosts.as_view(), name='my_likes'),
    path('add_image/', views.AddImage.as_view(), name='add_image'),
    path('profile/', views.profile_view, name='profile'),
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('category_view/<str:cats>', views.category_view, name='category_posts'),  # noqa
    path('delete_comment/<int:comment_id>', views.delete_comment,
         name='delete_comment'),
    path('<slug:slug>/', views.FeaturedPost.as_view(), name='featured_post'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('<slug:slug>/delete_post/', views.DeletePost.as_view(), name='delete_post'),  # noqa
    path('<slug:slug>/edit_post/', views.EditPost.as_view(), name='edit_post'),
]
