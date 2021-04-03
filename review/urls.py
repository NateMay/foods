from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [

    path('', views.ReviewLanding.as_view(), name='review_landing'),
    path('foods', views.FoodListView.as_view(), name='foods'),
    path('food/<int:pk>', views.FoodUpdate.as_view(), name='food_update'),
    path('pair/<int:pk>', views.FoodView.as_view(), name='food_usda'),
    # path('main/<int:pk>/delete', views.CatDelete.as_view(), name='cat_delete'),

    # path('lookup', views.BreedView.as_view(), name='breed_list'),
    # path('lookup/create', views.BreedCreate.as_view(), name='breed_create'),
    # path('lookup/<int:pk>/update', views.BreedUpdate.as_view(), name='breed_update'),
    # path('lookup/<int:pk>/delete', views.BreedDelete.as_view(), name='breed_delete')
]
