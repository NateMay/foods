from django import views
from django.urls import path
from .import views

app_name = 'review'
urlpatterns = [
    path('', views.ReviewLanding.as_view(), name='review_landing'),
    path('wiki_foods', views.FoodListView.as_view(), name='wiki_foods'),
    path('wiki_food/<int:pk>', views.FoodMetadataUpdate.as_view(), name='food_metadata'),
    path('pair_usda/<int:pk>', views.UsdaPairingView.as_view(), name='pair_usda'),

    path('wiki_categories', views.CategoriesListView.as_view(), name='wiki_categories'),
    path('wiki_category/<int:pk>', views.CategoryMetadataUpdate.as_view(), name='wiki_category'),

    path('pair/<int:pk>', views.PairedFoodView.as_view(), name='paired_food'),
    path('paired', views.PairedListView.as_view(), name='paired'),
    path('indexed', views.IndexedListView.as_view(), name='indexed'),
    
    path('food_scrape', views.ScrapeFood.as_view(), name='food_scrape'),
    path('category_scrape', views.ScrapeCategories.as_view(), name='category_scrape'),
    path('category_scrape/<int:pk>', views.ScrapeCategory.as_view(), name='test'),
    path('batch', views.Batch.as_view(), name='batch'),
]
