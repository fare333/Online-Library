from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path("register/",views.register_page,name="register"),
    path("logout/",views.sign_out,name="logout"),
    
    #Publisher
    path("about/",views.about,name="about"),
    path("publisher/",views.BookListView,name="publisher"),
    path("add-book/",views.post_book,name="post_book"),
    path("chats/",views.chat_list,name="chat_list"),
    path("search/",views.search,name="search"),
    path("feedback/",views.feedback,name="feedback"),
    path("book/<str:pk>/",views.view_book,name="book"),
    path("delete_request",views.delete_request,name="delete_request"),

    #Librarian
    path("librarian/",views.librarian,name="librarian"),
    path("recent_added_book/",views.recent_added_book,name="recent_added_book"),
    path("book_update/<str:pk>/",views.book_update,name="update"),
    path("book_delete/<str:pk>/",views.book_delete,name="delete"),
    
    #Admin
    path("dashboard/",views.dashboard,name="dashboard"),
    path("feedbacks/",views.feedbacks,name="feedbacks"),
    path("delete_requests/",views.delete_requests,name="delete_requests"),
    path("manage_books/",views.manage_books,name="manage_books"),
    path("users/",views.all_users,name="users"),
    path("delete_user/<str:pk>/",views.delete_user,name="delete_user"),
    path("edit_user/<str:pk>/",views.edit_user,name="edit_user"),
    path("user_details/<str:pk>/",views.user_details,name="user_details"),
    
]