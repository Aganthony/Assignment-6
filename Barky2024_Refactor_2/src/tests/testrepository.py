from django.test import TestCase
from djbarky.barkyapi.models import Bookmark as DjangoBookmark
from barky.domain import model as domain_model
from repository import DjangoRepository  # Adjust the import based on your actual structure

class DjangoRepositoryTestCase(TestCase):
    def setUp(self):
        self.repo = DjangoRepository()

    def test_add_bookmark(self):
        domain_bookmark = domain_model.Bookmark(title="Sample", url="http://example.com", notes="Test note")
        self.repo.add(domain_bookmark)
        self.assertTrue(DjangoBookmark.objects.exists())  # Ensure the bookmark is added
        self.assertEqual(DjangoBookmark.objects.get().title, "Sample")

    def test_get_bookmark(self):
        # Create a Django bookmark directly
        django_bookmark = DjangoBookmark.objects.create(title="Sample", url="http://example.com", notes="Test note")
        # Retrieve it using the repository
        retrieved_bookmark = self.repo.get(django_bookmark.id)
        self.assertIsNotNone(retrieved_bookmark)
        self.assertEqual(retrieved_bookmark.title, "Sample")

    def test_list_bookmarks(self):
        DjangoBookmark.objects.create(title="Sample1", url="http://example.com", notes="Test note")
        DjangoBookmark.objects.create(title="Sample2", url="http://example.org", notes="Another test note")
        bookmarks = self.repo.list()
        self.assertEqual(len(bookmarks), 2)
        self.assertEqual(bookmarks[0].title, "Sample1")
        self.assertEqual(bookmarks[1].title, "Sample2")

    def test_update_bookmark(self):
        django_bookmark = DjangoBookmark.objects.create(title="Sample", url="http://example.com", notes="Test note")
        domain_bookmark = domain_model.Bookmark(id=django_bookmark.id, title="Updated", url="http://example.com", notes="Updated note")
        self.repo.update(domain_bookmark)
        updated_bookmark = DjangoBookmark.objects.get(id=django_bookmark.id)
        self.assertEqual(updated_bookmark.title, "Updated")
        self.assertEqual(updated_bookmark.notes, "Updated note")

