from bookshelf.forms import BookForm, LoginForm, UserRegistrationForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from rest_framework import viewsets

from .serializers import BookSerializer
from .models import Book, Comment, Author


# from haystack.query import SearchQuerySet


def books(request):
    query = request.GET.get('query', '')
    search_query = request.GET.get('query', '')
    results = Book.objects.all()
    if search_query:
        # Создаем объект SearchQuery для выполнения поиска
        search_vector = SearchVector('title', 'author__name')

        # Создаем объект SearchQuery для запроса
        search_query = SearchQuery(search_query)
        trigram_similarity = TrigramSimilarity('title', query)
        trigram_similarity_author = TrigramSimilarity('author__name', query)
        # Выполняем поиск и упорядочиваем результаты по релевантности
        results = Book.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
            similarity=trigram_similarity + trigram_similarity_author
        ).filter(similarity__gt=0.3).order_by('-similarity')

    return render(request, 'bookshelf/index.html', {'books': results, 'query': query})


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
                    messages.add_message(request, messages.INFO, "Пользователь неактивен")
            else:
                messages.add_message(request, messages.INFO, "Неверные данные")
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

class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookCreateView(CreateView):
    template_name = 'bookshelf/book_create.html'
    form_class = BookForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


from rest_framework import generics


class BookViewSet(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailSet(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
