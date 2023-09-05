from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('add_image/', views.AddImage.as_view(), name='add_image'),
    path('<slug:slug>/', views.FeaturedPost.as_view(), name='featured_post'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('delete_post/', views.DeletePost.as_view(), name='delete_post'),
    path('edit_post/', views.EditPost.as_view(), name='edit_post')
]
