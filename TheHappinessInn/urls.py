from django.conf.urls import include,url
from django.contrib import admin
from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from management import views
from .feed import LatestEntriesFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('item/', views.ItemListView, name='item'),
    path('item/<int:pk>', views.ItemDetailView, name='item-detail'),
    path('item/create/', views.ItemCreate, name='item_create'),
    path('item/<int:pk>/update/', views.ItemUpdate, name='item_update'),
    path('item/<int:pk>/delete/', views.ItemDelete, name='item_delete'),

    path('customer/<int:pk>/delete/', views.CustomerDelete, name='customer_delete'),
    path('customer/create/', views.CustomerCreate, name='customer_create'),
    path('customer<int:pk>/update/', views.CustomerUpdate, name='customer_update'),
    path('customer/<int:pk>', views.CustomerDetail, name='customer_detail'),
    path('customer/', views.CustomertList, name='customer_list'),
    path('customer/order_customer', views.Customer_OrderListView, name='order_customer'),
    path('item/<int:pk>/order_issue/', views.Customer_Order_Issue, name='order_issue'),

    path('feed/', LatestEntriesFeed(), name='feed'),
    path('return/<int:pk>', views.ret, name='ret'),


url(r'^search_b/', views.search_item, name="search_i"),
url(r'^search_s/', views.search_customer, name="search_c")
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
