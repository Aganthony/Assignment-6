import sys
from abc import ABC, abstractmethod
from datetime import datetime

import requests

from database import DatabaseManager  # Ensure this import is correct

# Initialize DatabaseManager
db = DatabaseManager("bookmarks.db")

class Command(ABC):
    """
    Abstract base class for all commands.
    """
    @abstractmethod
    def execute(self, data=None):
        """
        Execute the command with the provided data.
        """
        raise NotImplementedError("Subclasses must implement this method")

class CreateBookmarksTableCommand(Command):
    """
    Command to create a bookmarks table in the database.
    """
    def execute(self, data=None):
        db.create_table(
            "bookmarks",
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            }
        )
        return "Bookmarks table created!"

class AddBookmarkCommand(Command):
    """
    Command to add a bookmark to the database.
    """
    def execute(self, data):
        if 'title' not in data or 'url' not in data:
            return "Error: Title and URL are required."
        data['date_added'] = datetime.utcnow().isoformat()  # Set current UTC datetime
        db.add("bookmarks", data)
        return "Bookmark added!"

class ListBookmarksCommand(Command):
    """
    Command to list bookmarks from the database, ordered by a specified column.
    """
    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        bookmarks = db.select("bookmarks", order_by=self.order_by)
        return bookmarks

class DeleteBookmarkCommand(Command):
    """
    Command to delete a bookmark from the database by ID.
    """
    def execute(self, data):
        if 'id' not in data:
            return "Error: ID is required for deletion."
        db.delete("bookmarks", {"id": data['id']})
        return "Bookmark deleted!"

class ImportGitHubStarsCommand(Command):
    """
    Command to import GitHub stars as bookmarks.
    """
    def execute(self, data):
        if 'github_username' not in data:
            return "Error: GitHub username is required."

        bookmarks_imported = 0
        next_page_of_results = f"https://api.github.com/users/{data['github_username']}/starred"

        while next_page_of_results:
            response = requests.get(next_page_of_results, headers={"Accept": "application/vnd.github.v3.star+json"})
            next_page_of_results = response.links.get("next", {}).get("url")

            for repo_info in response.json():
                bookmark_data = {
                    "title": repo_info["name"],
                    "url": repo_info["html_url"],
                    "notes": repo_info.get("description", "")
                }
                AddBookmarkCommand().execute(bookmark_data)
                bookmarks_imported += 1

        return f"Imported {bookmarks_imported} GitHub stars as bookmarks."

class EditBookmarkCommand(Command):
    """
    Command to update an existing bookmark.
    """
    def execute(self, data):
        if 'id' not in data:
            return "Error: ID is required for updating a bookmark."
        db.update("bookmarks", {"id": data['id']}, data)
        return "Bookmark updated!"

class QuitCommand(Command):
    """
    Command to quit the application.
    """
    def execute(self, data=None):
        print("Exiting application.")
        sys.exit()

