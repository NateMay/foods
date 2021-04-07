from django import views
from django.urls import path
from .import views

app_name = 'review'
urlpatterns = [
    path('', views.ReviewLanding.as_view(), name='review_landing'),
    path('foods', views.FoodListView.as_view(), name='foods'),
    path('food_metadata/<int:pk>', views.FoodMetadataUpdate.as_view(), name='food_metadata'),
    path('pair/<int:pk>', views.UsdaPairingView.as_view(), name='food_usda'),
    path('complete/<int:pk>', views.CompleteFoodView.as_view(), name='complete_food'),
    path('completed', views.CompletedListView.as_view(), name='completed'),
    path('food_scrape', views.ScrapeFood.as_view(), name='food_scrape'),
    path('category_scrape', views.ScrapeCategories.as_view(), name='category_scrape'),
    path('categories', views.CategoryList.as_view(), name='categories'),
    path('batch', views.Batch.as_view(), name='batch'),
    # path('scrape_cat', views2.ScrapeCategory.as_view(), name='scrape_cat'),
]
