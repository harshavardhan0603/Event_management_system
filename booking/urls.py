from booking import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.index, name='index'),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('sign_up/', views.registerpage, name = "signup" ),
    path('contact/', views.contact , name= "contact" ),
    path('book/', views.book , name= "book" ),
    path('view_venues/',views.view, name= "view"),
    path('history/',views.history,name= "hist"),
    path('review/',views.review, name= "review"),
    path("update/<str:n>", views.update, name = "update"),
    path("delete/<str:n>", views.delete, name = "delete"),
    path("feedback/<str:n>", views.feedback, name = "feedback"),
    path("receipt/<str:n>", views.receipt, name = "receipt"),
    # path("payment/", views.order_payment, name="payment"),
    # path("reciept/", views.pdf_report_create, name = "reciept")

]

