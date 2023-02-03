from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import User, Book, Chat, DeleteRequest, Feedback
from django.db.models import Sum
from .forms import ChatForm, BookForm, UserForm,RegisterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout,login
from django.contrib import auth, messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request,user)
            if user.is_admin or user.is_superuser:
                return redirect("dashboard")
            elif user.is_librarian:
                return redirect("librarian")
            else:
                return redirect("publisher")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
        
    return render(request, "bookstore/login.html")

@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect("login")


def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Registration fail, try again later')
            return redirect('login')
    
    form = RegisterForm()
    context = {"form":form}
    return render(request, "bookstore/register.html", context)


#Publisher
@login_required(login_url='login')
def publisher(request):
    return render(request, 'publisher/home.html')

@login_required(login_url='login')
def about(request):
    return render(request, 'publisher/about.html')

@login_required(login_url='login')
def search(request):
    query = request.GET.get("query","")
    books = Book.objects.filter(Q(title__icontains=query))
    page = request.GET.get('page', 1)

    paginator = Paginator(books, 2)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        
    context = {"books":books,"paginator":paginator,"query":query}
    return render(request, 'publisher/book_list.html',context)


@login_required(login_url='login')
def feedback(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback")
        user = request.user.username
        feedback = f"{user} says {feedback}"
        if feedback:
            Feedback.objects.create(feedback=feedback)
            messages.success(request, 'Feedback was sent successfully')
            return redirect('feedback')
    return render(request,'publisher/feedback.html')
    

@login_required(login_url='login')
def chat_list(request):
    chat_list = Chat.objects.filter(posted_at__lt=timezone.now())
    
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("chat_list")
    
    context = {"chat_list":chat_list}
    return render(request, 'publisher/chat_list.html',context)
    

@login_required(login_url='login')
def post_book(request):
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book was added successfully')
            if request.user.is_publisher:
                return redirect('publisher')
            elif request.user.is_librarian:
                return redirect('librarian')
        else:
            messages.error(request, 'Book was not added, try again later')
    
    context = {"form":form}
    return render(request, 'publisher/post_book.html',context)

@login_required(login_url='login')
def delete_request(request):
    if request.method == "POST":
        book = int(request.POST.get("book"))
        request_delete = request.POST.get("delete_request")
        DeleteRequest.objects.create(book_id=book,delete_request=request_delete)
        messages.success(request, 'Request was sent successfully')
        return redirect('book',pk=book)

@login_required(login_url='login')
def view_book(request,pk):
    book = Book.objects.get(pk=pk)
    context = {"object":book}
    return render(request, 'publisher/views_book.html',context)

#Librarian
@login_required(login_url='login')
def librarian(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    context = {"book":book,"user":user}
    return render(request, 'librarian/home.html',context)

@login_required(login_url='login')
def recent_added_book(request):
    books = Book.objects.all()[:5]
    context = {"books":books}
    return render(request, 'librarian/recent_added_book.html',context)

@login_required(login_url='login')
def book_delete(request,pk):
    if request.user.is_librarian or request.user.is_superuser or request.user.is_staff:
        book = Book.objects.get(pk=pk)
        book.delete()
        messages.success(request, 'Book was deleted successfully')
        return redirect('publisher')

@login_required(login_url='login')
def book_update(request,pk):
    if request.user.is_librarian or request.user.is_superuser or request.user.is_staff:
        book = Book.objects.get(pk=pk)
        form = BookForm(instance=book)
        if request.method == "POST":
            form = BookForm(request.POST,request.FILES,instance=book)
            if form.is_valid():
                form.save()
                messages.success(request,"The update is successful")
                return redirect('book',pk=book.pk)
        context = {"form":form}
        return render(request, 'librarian/book_update.html',context)
    else:
        return redirect('publisher')
#Admin views
@login_required(login_url='login')
def dashboard(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    context = {"book":book,"user":user}   
    return render(request, 'dashboard/home.html',context)

@login_required(login_url='login')
def BookListView(request):
    books = Book.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(books, 2)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context = {'books':books,"paginator":paginator}
    return render(request, 'publisher/book_list.html',context)

@login_required(login_url='login')
def feedbacks(request):
    feedbacks = Feedback.objects.all()
    context = {"feedbacks":feedbacks}
    return render(request, 'dashboard/feedbacks.html',context)

@login_required(login_url='login')
def delete_requests(request):
    requests = DeleteRequest.objects.all()
    context = {"requests":requests}
    return render(request, 'dashboard/requests.html',context)

@login_required(login_url='login')
def manage_books(request):
    books = Book.objects.all()
    context = {"books":books}
    return render(request, 'publisher/book_list.html',context)

@login_required(login_url='login')
def all_users(request):
    users = User.objects.all()
    context = {"users":users}
    return render(request, 'dashboard/users.html',context)

@login_required(login_url='login')
def delete_user(request,pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect("users")

@login_required(login_url='login')
def edit_user(request,pk):
    user = User.objects.get(pk=pk)
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"The update is successful")
            return redirect('users')
    context = {"form":form}
    return render(request, 'dashboard/user_edit.html',context)

@login_required(login_url='login')
def user_details(request,pk):
    user = User.objects.get(pk=pk)
    context = {"object":user}
    return render(request, 'dashboard/user_details.html',context)
    