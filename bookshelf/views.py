from bookshelf.forms import SearchForm, BookForm, LoginForm, UserRegistrationForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
# from haystack.query import SearchQuerySet

from .models import Book, Comment


def books(request):
    # form = SearchForm()
    # if 'query' in request.GET:
    #     form = SearchForm(request.GET)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         results = SearchQuerySet().models(Book).filter(title=cd['query']).load_all()
    #         # count total results
    #         total_results = results.count()
    return render(request, 'bookshelf/index.html', {'books': Book.objects.all()})


def remove_book(request):
    if 'id' in request.POST:
        Book.objects.filter(pk=int(request.POST['id'])).first().delete()
    return redirect('main')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.INFO, "Успешно авторизован")
                    return redirect('main')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'bookshelf/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            login(request, user)
            messages.add_message(request, messages.INFO, "Вы успешно зарегистрировались")
            return redirect('main')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'bookshelf/register.html', {'user_form': user_form})


def write_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            if 'user' in request.POST and 'book' in request.POST:
                Comment(author=User.objects.filter(username=request.POST['user']).first(),
                        book=Book.objects.filter(pk=request.POST['book']).first(), text=cd['text']).save()
                messages.add_message(request, messages.INFO, "Комментарий оставлен")
    return redirect(request.META.get('HTTP_REFERER'))


class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'published_date', 'description', 'cover']
    template_name = 'bookshelf/book_update.html'
    success_url = reverse_lazy('main')


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(book=self.object).all()
        context['comment_form'] = CommentForm()
        return context


class BookCreateView(CreateView):
    template_name = 'bookshelf/book_create.html'
    form_class = BookForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
