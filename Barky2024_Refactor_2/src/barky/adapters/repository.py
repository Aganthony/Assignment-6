from typing import Set
import abc
from barky.domain import model
from djbarky.barkyapi import models as django_models

class AbstractRepository(abc.ABC):
    """
    An abstract base class for repository implementations. 
    This abstract repository can be used with any data storage strategy.
    """

    def __init__(self):
        self.seen: Set[model.Bookmark] = set()

    def add(self, bookmark: model.Bookmark):
        self._add(bookmark)
        self.seen.add(bookmark)

    def get(self, bookmark_id) -> model.Bookmark:
        bookmark = self._get(bookmark_id)
        if bookmark:
            self.seen.add(bookmark)
        return bookmark

    @abc.abstractmethod
    def _add(self, bookmark: model.Bookmark):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, bookmark_id) -> model.Bookmark:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[model.Bookmark]:
        raise NotImplementedError

class DjangoRepository(AbstractRepository):
    """
    A Django ORM-based implementation of the repository.
    """

    def _add(self, bookmark: model.Bookmark):
        django_model = django_models.Bookmark.objects.create(
            title=bookmark.title,
            url=bookmark.url,
            notes=bookmark.notes
        )
        bookmark.id = django_model.id  # Assume the domain model has an `id` attribute.

    def _get(self, bookmark_id) -> model.Bookmark:
        django_bookmark = django_models.Bookmark.objects.filter(id=bookmark_id).first()
        return django_bookmark.to_domain() if django_bookmark else None

    def list(self) -> list[model.Bookmark]:
        return [b.to_domain() for b in django_models.Bookmark.objects.all()]

    def update(self, bookmark: model.Bookmark):
        django_bookmark = django_models.Bookmark.objects.filter(id=bookmark.id).first()
        if django_bookmark:
            django_bookmark.title = bookmark.title
            django_bookmark.url = bookmark.url
            django_bookmark.notes = bookmark.notes
            django_bookmark.save()
