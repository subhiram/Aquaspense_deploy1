from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing_page, name='product'),
    path('addcrop/<pk>', views.create_crop,name='new_crop'),
    path('maindash/<pk>/',views.crop_main_dashboard, name='main_dash'),  #main dashboard url
    #path('sub/<pk>/',views.crop_sub_dashboard),
    path('add_expense/<pk>/',views.create_expense),
    path('add_workerexp/<pk>/',views.create_workerexp),
    path('add_feed/<pk>/',views.create_feed),
    path('add_medicine/<pk>/',views.create_medicine),
    path('add_elebill/<pk>/',views.create_elebill),
    path('add_export/<pk>/',views.create_export),
    path('add_daily_feed/<pk>/',views.create_daily_feed),
    path('complete_view/<pk>/', views.complete_view, name='complete_view'),
    #path('insight/<pk>/',views.insight),
    #path('hh/',views.chart_view),
    path('graph/<pk>/',views.graphs),
    path('delete/<str:name>/<pk>/', views.delete),
    path('dashboard/<pk>/',views.dashboard),
    path('signup/',views.signup),
    path('login/', views.user_login,name='login'),
    path('logout', views.user_logout, name='logout'),
    #path('add_data/<pk>/', views.add_data),
    path('main_graph/<pk>/', views.maindash_graph),
    path('complete_crop/<pk>/<days>/',views.complete_btn_update),
    path('profile/<pk>/', views.profile),
    path('estimate/<pk>/', views.estimate),
    path('verify/', views.verify, name="verify"),
]