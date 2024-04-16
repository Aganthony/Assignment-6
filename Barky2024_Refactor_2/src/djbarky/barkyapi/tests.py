from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Snippet
from .models import Bookmark
from .views import BookmarkViewSet
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Bookmark
from .views import BookmarkViewSet

# Create your tests here.
# test plan

class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }        
        response = self.client.put(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")


    # 6. create a snippet
        
 # 6. create a snippet
class SnippetTestCase(APITestCase):
    
    def test_create_snippet(self):
        """
        Ensure we can create a new snippet.
        """
        url = reverse('snippet-list')
        data = {'title': 'Sample Snippet', 'code': 'print("hello, world")'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Snippet.objects.get().title, 'Sample Snippet')
 
    # 7. retrieve a snippet
    def test_retrieve_snippet(self):
        """
        Ensure we can retrieve a snippet.
        """
        snippet = Snippet.objects.create(title='Sample Snippet', code='print("hello, world")')
        url = reverse('snippet-detail', args=[snippet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Snippet')
    # 8. delete a snippet
    def test_delete_snippet(self):
        """
        Ensure we can delete a snippet.
        """
        snippet = Snippet.objects.create(title='Sample Snippet', code='print("hello, world")')
        url = reverse('snippet-detail', args=[snippet.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)

    
    # 9. list snippets
 
    def test_list_snippets(self):
        """
        Ensure we can list all snippets.
        """
        # Create a couple of snippets
        Snippet.objects.create(title='Snippet One', code='print("First snippet")')
        Snippet.objects.create(title='Snippet Two', code='print("Second snippet")')
        
        # Make a request to the list endpoint
        response = self.client.get(reverse('snippet-list'))
        
        # Check if the response is successful and contains 2 snippets
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
       
    # 10. update a snippet
    def test_update_snippet(self):
        """
        Ensure we can update a snippet.
        """
        snippet = Snippet.objects.create(title='Sample Snippet', code='print("hello, world")')
        url = reverse('snippet-detail', args=[snippet.id])
        data = {'title': 'Updated Snippet', 'code': 'print("hello, world")'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snippet.refresh_from_db()
        self.assertEqual(snippet.title, 'Updated Snippet')
        
# 11. create a user
class UserTestCase(APITestCase):
    
    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('user-list')  # Replace 'user-list' with your actual URL name for creating users
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        # Check that the response indicates a successful creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify that the User was indeed added to the database
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
      

# 12. retrieve a user
        
class UserTestCase(APITestCase):
    
    def setUp(self):
        # Create a user that we'll retrieve later in the test
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword123')
        self.user_url = reverse('user-detail', kwargs={'pk': self.user.pk})  # Adjust 'user-detail' and 'pk' as needed

    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user's details.
        """
        response = self.client.get(self.user_url)
        
        # Check that the response indicates success
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the response data matches the user we created
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

# 13. delete a user

class UserTestCase(APITestCase):
    
    def setUp(self):
        # Create a user to be deleted later
        self.user = User.objects.create_user(username='deleteuser', email='delete@example.com', password='testpass123')
        self.delete_url = reverse('user-detail', kwargs={'pk': self.user.pk})  # Adjust 'user-detail' as needed

    def test_delete_user(self):
        """
        Ensure we can delete a user.
        """
        # Initial count
        initial_user_count = User.objects.count()
        
        # Perform the delete operation
        response = self.client.delete(self.delete_url)
        
        # Check that the response indicates a successful deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Ensure the user count has decreased by 1
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, initial_user_count - 1)

        # Optionally, verify the user has been deleted and cannot be retrieved
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
  

# 14. list users
class UserListTestCase(APITestCase):
    def test_list_users(self):
        """
        Ensure we can list all users.
        """
        User.objects.create_user('user1', 'user1@example.com', 'password')
        User.objects.create_user('user2', 'user2@example.com', 'password')
        response = self.client.get(reverse('user-list'))  # Adjust URL name as necessary
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Adjust according to response structure


# 15. update a user
        
class UserUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('updateuser', 'update@example.com', 'password')
        self.update_url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def test_update_user(self):
        """
        Ensure we can update a user's details.
        """
        data = {'username': 'updateduser', 'email': 'update@example.com', 'password': 'newpassword'}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

# 16. highlight a snippet
class SnippetHighlightTestCase(APITestCase):
    def setUp(self):
        self.snippet = Snippet.objects.create(code='print("Hello, world")')
        self.highlight_url = reverse('snippet-highlight', kwargs={'pk': self.snippet.pk})

    def test_highlight_snippet(self):
        """
        Ensure we can highlight a snippet.
        """
        response = self.client.post(self.highlight_url)  # Assuming POST is used for highlighting
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.snippet.refresh_from_db()
        self.assertTrue(self.snippet.highlighted)  # Assuming 'highlighted' is a model field

# 17. list bookmarks by user
class BookmarkListByUserTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'password')
        Bookmark.objects.create(title="Bookmark 1", user=self.user1)
        Bookmark.objects.create(title="Bookmark 2", user=self.user2)
        self.list_by_user_url = reverse('bookmark-list-by-user', kwargs={'user_id': self.user1.id})

    def test_list_bookmarks_by_user(self):
        """
        Ensure we can list bookmarks by a specific user.
        """
        response = self.client.get(self.list_by_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Adjust according to response structure

# 18. list snippets by user
class SnippetListByUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('snippetuser', 'snippet@example.com', 'password')
        Snippet.objects.create(code='print("Hello, world")', owner=self.user)
        self.list_by_user_url = reverse('snippet-list-by-user', kwargs={'user_id': self.user.id})

    def test_list_snippets_by_user(self):
        """
        Ensure we can list snippets created by a specific user.
        """
        response = self.client.get(self.list_by_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# 20. list bookmarks by date
class BookmarkListByDateTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('dateuser', 'date@example.com', 'password')
        Bookmark.objects.create(title="Bookmark Date 1", user=user, date_added='2023-01-01')
        self.list_by_date_url = reverse('bookmark-list-by-date', kwargs={'date': '2023-01-01'})

    def test_list_bookmarks_by_date(self):
        """
        Ensure we can list bookmarks added on a specific date.
        """
        response = self.client.get(self.list_by_date_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# 21. list snippets by date
class SnippetListByDateTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('datesnippetuser', 'datesnippet@example.com', 'password')
        Snippet.objects.create(code='print("Hello, Date")', owner=user, created='2023-01-01')
        self.list_by_date_url = reverse('snippet-list-by-date', kwargs={'date': '2023-01-01'})

    def test_list_snippets_by_date(self):
        """
        Ensure we can list snippets created on a specific date.
        """
        response = self.client.get(self.list_by_date_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# 23. list bookmarks by title
class BookmarkListByTitleTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('titleuser', 'title@example.com', 'password')
        Bookmark.objects.create(title="Specific Title", user=user)
        self.list_by_title_url = reverse('bookmark-list-by-title', kwargs={'title': 'Specific Title'})

    def test_list_bookmarks_by_title(self):
        """
        Ensure we can list bookmarks with a specific title.
        """
        response = self.client.get(self.list_by_title_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(bookmark['title'] == 'Specific Title' for bookmark in response.data))


# 24. list snippets by title
class SnippetListByTitleTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('titlesnippetuser', 'titlesnippet@example.com', 'password')
        Snippet.objects.create(title="Unique Title", code='print("Title")', owner=user)
        self.list_by_title_url = reverse('snippet-list-by-title', kwargs={'title': 'Unique Title'})

    def test_list_snippets_by_title(self):
        """
        Ensure we can list snippets with a specific title.
        """
        response = self.client.get(self.list_by_title_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(snippet['title'] == 'Unique Title' for snippet in response.data))

# 26. list bookmarks by url
class BookmarkListByURLTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('urluser', 'url@example.com', 'password')
        Bookmark.objects.create(title="Bookmark URL", url="https://example.com", user=user)
        self.list_by_url_url = reverse('bookmark-list-by-url', kwargs={'url': 'https://example.com'})

    def test_list_bookmarks_by_url(self):
        """
        Ensure we can list bookmarks with a specific URL.
        """
        response = self.client.get(self.list_by_url_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(bookmark['url'] == 'https://example.com' for bookmark in response.data))


# 27. list snippets by url

User = get_user_model()

class SnippetListByURLTestCase(APITestCase):
    def setUp(self):
        # Setup user and snippets with URLs
        user = User.objects.create_user('testuser', 'test@example.com', 'password')
        Snippet.objects.create(code='print("Hello, world")', owner=user, url="https://example.com/snippet1")
        Snippet.objects.create(code='print("Goodbye, world")', owner=user, url="https://example.com/snippet2")
        Snippet.objects.create(code='print("Another URL")', owner=user, url="https://otherdomain.com/snippet")

        self.list_by_url_url = reverse('snippet-list-by-url', kwargs={'url': 'https://example.com'})

    def test_list_snippets_by_url(self):
        """
        Ensure we can list snippets with a specific URL.
        """
        response = self.client.get(self.list_by_url_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #  API returns a list of snippets directly
        snippets = response.data
        self.assertEqual(len(snippets), 2)  
        
        #  returned snippets indeed have the specified URL
        for snippet in snippets:
            self.assertIn("https://example.com", snippet['url'])

