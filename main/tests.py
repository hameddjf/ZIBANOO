from unittest.mock import patch
from django.utils.translation import activate
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.test.client import RequestFactory
from django.forms import CharField
from django import template
from django.contrib.auth import get_user_model

from .models import Base
from .tasks import send_notification_email, update_view_count
from .middleware import LanguageMiddleware, ViewCountMiddleware
from .utils import custom_slugify, get_unique_slug, get_client_ip
from .templatetags.custom_tags import truncate_chars, get_verbose_name, addclass, highlight_search

from tags.models import Category, Tag


User = get_user_model()


class BaseModelTest(TestCase):
    """Test case for the Base model"""

    def setUp(self):
        """Set up test data for Base model tests"""
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')

    def test_base_creation(self):
        """Test Base object creation and its attributes"""
        base = Base.objects.create(
            title='Test Base',
            content='This is a test content',
            user=self.user
        )
        base.category.add(self.category)
        base.tags.add(self.tag)

        self.assertEqual(base.title, 'Test Base')
        self.assertEqual(base.content, 'This is a test content')
        self.assertEqual(base.user, self.user)
        self.assertEqual(base.category.first(), self.category)
        self.assertEqual(base.tags.first(), self.tag)
        self.assertFalse(base.is_published)
        self.assertEqual(base.view_count, 0)
        self.assertEqual(base.like_count, 0)

    def test_base_methods(self):
        """Test Base model methods"""
        base = Base.objects.create(
            title='Test Base Methods',
            content='This is a test content for methods',
            user=self.user
        )

        base.increment_view_count()
        self.assertEqual(base.view_count, 1)

        base.like()
        self.assertEqual(base.like_count, 1)

        self.assertEqual(str(base), 'Test Base Methods')


class CustomTagsTestCase(TestCase):
    """Test case for the Base templatetags"""

    def test_truncate_chars(self):
        """Test truncate_chars function"""
        self.assertEqual(truncate_chars("Hello World", 5), "Hello...")
        self.assertEqual(truncate_chars("Hello", 5), "Hello")
        self.assertEqual(truncate_chars("Hello World", 7), "Hello...")

    def test_get_verbose_name(self):
        """Test get_verbose_name function"""
        class TestModel:
            class _meta:
                def get_field(self, field_name):
                    class Field:
                        verbose_name = "test field"
                    return Field()

        instance = TestModel()
        self.assertEqual(get_verbose_name(instance, "test"), "Test Field")

    def test_addclass(self):
        """Test addclass filter"""
        field = CharField()
        result = addclass(field, "test-class")
        self.assertIn('class="test-class"', result)

    def test_highlight_search(self):
        """Test highlight_search filter"""
        result = highlight_search("Hello World", "World")
        self.assertEqual(result, 'Hello <span class="highlight">World</span>')


class UtilsTestCase(TestCase):
    """Test case for the Base utils"""

    def test_custom_slugify(self):
        """Test custom_slugify function"""
        self.assertEqual(custom_slugify("Hello World!"), "hello-world")
        self.assertEqual(custom_slugify("This is a test"), "this-is-a-test")

    def test_get_unique_slug(self):
        """Test get_unique_slug function"""
        class TestModel:
            title = "Test Title"
            slug = ""

            class _default_manager:
                @staticmethod
                def filter(**kwargs):
                    class QuerySet:
                        def exists(self):
                            return False
                    return QuerySet()

        instance = TestModel()
        slug = get_unique_slug(instance, "title", "slug")
        self.assertEqual(slug, "test-title")

    def test_get_client_ip(self):
        """Test get_client_ip function"""
        factory = RequestFactory()
        request = factory.get('/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        self.assertEqual(get_client_ip(request), '127.0.0.1')

        request.META['HTTP_X_FORWARDED_FOR'] = '10.0.0.1'
        self.assertEqual(get_client_ip(request), '10.0.0.1')


class MiddlewareTestCase(TestCase):
    """Test case for the Base middleware"""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_language_middleware(self):
        """Test LanguageMiddleware"""
        middleware = LanguageMiddleware(get_response=lambda r: None)
        request = self.factory.get('/')
        request.session = {}
        middleware.process_request(request)
        self.assertEqual(request.session.get('django_language'), 'fa')

    def test_view_count_middleware(self):
        """Test ViewCountMiddleware"""
        middleware = ViewCountMiddleware(get_response=lambda r: None)
        request = self.factory.get('/')
        request.user = self.user
        response = type('Response', (), {
                        'status_code': 200, 'context_data': {'object': self.user}})()
        middleware.process_response(request, response)


class TasksTestCase(TestCase):
    """Test case for the Base tasks"""

    @patch('.tasks.send_mail')
    def test_send_notification_email(self, mock_send_mail):
        """Test send_notification_email task"""
        send_notification_email(
            "Test Subject", "Test Message", ["test@example.com"])
        mock_send_mail.assert_called_once_with(
            "Test Subject",
            "Test Message",
            settings.DEFAULT_FROM_EMAIL,
            ["test@example.com"],
            fail_silently=False,
        )

    @patch('.tasks.apps.get_model')
    def test_update_view_count(self, mock_get_model):
        """Test update_view_count task"""
        class MockModel:
            view_count = 0

            def save(self):
                pass

        mock_object = MockModel()
        mock_get_model.return_value.objects.get.return_value = mock_object

        update_view_count("TestModel", 1)
        self.assertEqual(mock_object.view_count, 1)
