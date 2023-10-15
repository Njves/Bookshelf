from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author, Comment


class BookshelfViewsTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Создаем тестовую книгу
        self.book = Book.objects.create(
            title='Test Book',
            author=Author.objects.create(name='Test Author', birth_day='2022-01-01'),
            published_date='2022-01-01',
            description='Test Description',
            cover='test_cover.jpg'
        )

        # Создаем тестовый комментарий
        self.comment = Comment.objects.create(
            author=self.user,
            book=self.book,
            text='Test Comment'
        )

        # Создаем тестовый клиент
        self.client = Client()

    def test_books_view(self):
        # Проверяем, что страница доступна
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_view(self):
        # Проверяем, что страница доступна
        response = self.client.get(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что информация о книге отображается
        self.assertContains(response, 'Test Book')

    def test_book_create_view(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpass')
        # Проверяем, что страница доступна
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма отображается
        self.assertContains(response, '<form')

    def test_book_update_view(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpass')
        # Проверяем, что страница доступна
        response = self.client.get(reverse('edit', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма отображается
        self.assertContains(response, '<form')

    def test_author_detail_view(self):
        # Проверяем, что страница доступна
        response = self.client.get(reverse('author-detail', args=[self.book.author.id]))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что информация об авторе отображается
        self.assertContains(response, 'Test Author')

    def test_user_login_view(self):
        # Проверяем, что страница доступна
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма отображается
        self.assertContains(response, '<form')

    def test_user_logout_view(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpass')
        # Проверяем, что после выхода из системы происходит перенаправление на главную страницу
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('main'))

    def test_user_registration_view(self):
        # Проверяем, что страница доступна
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма отображается
        self.assertContains(response, '<form')

