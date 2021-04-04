from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [

    path('', views.ReviewLanding.as_view(), name='review_landing'),
    path('foods', views.FoodListView.as_view(), name='foods'),
    path('food_metadata/<int:pk>', views.FoodMetadataUpdate.as_view(), name='food_metadata'),
    path('pair/<int:pk>', views.UsdaPairingView.as_view(), name='food_usda'),
    # path('main/<int:pk>/delete', views.CatDelete.as_view(), name='cat_delete'),

]
