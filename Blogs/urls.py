from django.urls import path, include
from Blogs.views import SoBlogsView,Get_detail_Blogs,Get_Blog_Filter
urlpatterns =[
    path('blogs/home', SoBlogsView.as_view(), name='so_blogs'),
    path('blogs/detail/<str:id>', Get_detail_Blogs.as_view(), name='get_detail_blogs'),
    path('blogs/filter', Get_Blog_Filter.as_view(), name='get_blog_filter'),
]