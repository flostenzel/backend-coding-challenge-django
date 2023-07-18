from authors.models import Author
from model_bakery import baker
from notes.models import Note, Tag
from rest_framework import status

from app.tests.utils import APIViewTest


class TestNoteCreateView(APIViewTest):
    """
    Test cases for the `NoteCreateView` API view.
    """
    url = '/notes/note/create/'

    def test_successful_create_note(self):
        """
        Test successful creation of a note without tags.
        """
        data = {
            "title": "Test Title",
            "body": "This is a test message",
            "tags": [],
            "is_public": False,
        }
        response = self.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_successful_create_note_with_tag(self):
        """
        Test successful creation of a note with tags.
        """
        tags = baker.make(Tag, _quantity=2)
        data = {
            "title": "Test Title",
            "body": "This is a test message",
            "tags": [str(tags[0].pk), str(tags[1].pk)],
            "is_public": False,
        }
        response = self.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(author=self.auth_user)
        self.assertEqual(set(note.tags.all()), set(tags))

    def test_create_note_without_being_logged_in(self):
        """
        Test creation of a note without being logged in (should fail).
        """
        data = {
            "title": "Test Title",
            "body": "This is a test message",
            "tags": [],
            "is_public": False,
        }
        self.auth_user.delete()
        response = self.post(self.url, data, auth=None, expect_errors=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestNoteListView(APIViewTest):
    """
    Test cases for the `NoteListView` API view.
    """
    url = '/notes/note/list/'

    def test_get_list_of_public_notes_as_non_auth_user(self):
        """
        Test retrieval of a list of public notes as a non-authenticated user.
        Only public notes should be returned.
        """
        baker.make(Note, _quantity=5, is_public=False)
        baker.make(Note, _quantity=5, is_public=True)
        baker.make(Note, _quantity=5, author=self.auth_user)
        self.auth_user.delete()
        response = self.app.get(url=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json), 5)

    def test_only_show_notes_of_author(self):
        """
        Test retrieval of only the notes of the authenticated user.
        """
        baker.make(Note, _quantity=5)
        baker.make(Note, _quantity=5, author=self.auth_user)
        response = self.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json), 5)

    def test_search_for_content_of_the_body(self):
        """
        Test search for notes based on the content of the body.
        Notes containing the searched keyword should be returned.
        """
        baker.make(Note, body="test this body", author=self.auth_user)
        baker.make(Note, body="This is the second test", author=self.auth_user)
        baker.make(Note, body="Not included", _quantity=5, author=self.auth_user)
        first_response = self.get(f"{self.url}?search=test")
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(first_response.json), 2)


class TestNoteListViewWithTag(APIViewTest):
    """
    Test cases for the `NoteListView` API view when searching for tags.
    """
    url = '/notes/note/list/'

    def setUp(self):
        super().setUp()

        self.first_tag = baker.make(Tag)
        baker.make(Note, tags=[self.first_tag], author=self.auth_user, _quantity=2, body="test")

        self.second_tag = baker.make(Tag)
        baker.make(Note, tags=[self.first_tag, self.second_tag], author=self.auth_user)
        baker.make(Note, tags=[self.second_tag], author=self.auth_user, body="This is a test")

        self.third_tag = baker.make(Tag)
        baker.make(Note, tags=[self.third_tag], author=self.auth_user, _quantity=10)
        baker.make(Note, _quantity=5, author=self.auth_user)

    def test_search_for_first_tag(self):
        """
        Test search for notes with the first tag.
        The response should include all notes associated with the first tag.
        """
        response_first_tag = self.get(f'{self.url}?tag={self.first_tag.pk}')
        self.assertEqual(len(response_first_tag.json), 3)

    def test_search_for_second_tag(self):
        """
        Test search for notes with the second tag.
        The response should include all notes associated with the second tag.
        """
        response_first_tag = self.get(f'{self.url}?tag={self.second_tag.pk}')
        self.assertEqual(len(response_first_tag.json), 2)

    def test_search_for_third_tag(self):
        """
        Test search for notes with the third tag.
        The response should include all notes associated with the third tag.
        """
        response_first_tag = self.get(f'{self.url}?tag={self.third_tag.pk}')
        self.assertEqual(len(response_first_tag.json), 10)

    def test_search_for_first_and_second_tag(self):
        """
        Test search for notes with both the first and second tags.
        The response should include only the notes associated with both tags.
        """
        response_first_tag = self.get(f'{self.url}?tag={self.first_tag.pk}+{self.second_tag.pk}')
        self.assertEqual(len(response_first_tag.json), 1)

    def test_search_for_content_and_tag(self):
        """
        Test search for notes with both the first and second tags.
        The response should include only the notes associated with both tags.
        """
        response_first_tag = self.get(f'{self.url}?search=test&tag={self.second_tag.pk}')
        self.assertEqual(len(response_first_tag.json), 1)


class TestNoteDetailView(APIViewTest):
    """
    Test cases for the `NoteDetailView` API view.
    """
    url = '/notes/note/{}/'

    def test_get_detail_of_note(self):
        """
        Test retrieval of the detail of a note.
        The response should include the note's ID and title.
        """
        note = baker.make(Note, author=self.auth_user)
        response = self.get(self.url.format(note.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json['id'], note.pk)
        self.assertEqual(response.json['title'], note.title)

    def test_add_tag_to_note(self):
        """
        Test adding a tag to a note.
        """
        note = baker.make(Note, author=self.auth_user)
        tag = baker.make(Tag)
        data = {"tag": str(tag.pk)}
        response = self.patch(self.url.format(note.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json['id'], note.pk)
        self.assertEqual(response.json['title'], note.title)

    def test_update_title_of_note(self):
        """
        Test updating the title of a note.
        The note's title should be updated to the new title provided.
        """
        note = baker.make(Note, title="test", author=self.auth_user)
        data = {"title": "changed title"}
        response = self.patch(self.url.format(note.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(response.json['id'], note.pk)
        self.assertEqual(response.json['title'], note.title)
        self.assertEqual(response.json['title'], data["title"])

    def test_update_note_from_other_author(self):
        """
        Test updating a note from another author (should fail).
        Only the author of a note should be able to update it.
        """
        new_author = baker.make(Author)
        note = baker.make(Note, title="test", author=new_author)
        data = {"title": "changed title"}
        response = self.patch(self.url.format(note.pk), data, expect_errors=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note(self):
        """
        Test deletion of a note.
        The note should be deleted and no longer exist in the database.
        """
        note = baker.make(Note, author=self.auth_user)
        response = self.delete(self.url.format(note.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.all())

    def test_delete_note_from_other_author(self):
        """
        Test deletion of a note from another author (should fail).
        Only the author of a note should be able to delete it.
        """
        new_author = baker.make(Author)
        note = baker.make(Note, author=new_author)
        response = self.delete(self.url.format(note.pk), expect_errors=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Note.objects.all())


class TestCreateTagView(APIViewTest):
    """
    Test cases for the `CreateTagView` API view.
    """
    url = '/notes/tag/create/'

    def test_create_tag(self):
        """
        Test creation of a tag.
        """
        data = {"title": "test title"}
        self.assertFalse(Tag.objects.all())
        self.post(self.url, data)
        self.assertTrue(Tag.objects.all())


class TestTagDetailView(APIViewTest):
    """
    Test cases for the `TagDetailView` API view.
    """
    url = '/notes/tag/{}/'

    def test_change_tag(self):
        """
        Test changing the title of a tag.
        The title of the tag should be updated to the new title provided.
        """
        new_tag = baker.make(Tag, title="title")
        data = {"title": "new_title"}
        baker.make(Note, tags=[new_tag], author=self.auth_user)
        baker.make(Note, _quantity=5, author=self.auth_user)
        response = self.patch(self.url.format(new_tag.pk), data=data)
        self.assertEqual(response.json["title"], data["title"])


class TestTagListView(APIViewTest):
    """
    Test cases for the `TagListView` API view.
    """
    url = '/notes/tag/list/'

    def test_get_all_tag(self):
        """
        Test retrieval of all tags.
        """
        first_tag = baker.make(Tag, title="title")
        second_tag = baker.make(Tag, title="title")
        baker.make(Tag, title="title")
        baker.make(Note, tags=[first_tag, second_tag], author=self.auth_user)
        baker.make(Note, _quantity=5, author=self.auth_user)
        response = self.get(self.url)
        self.assertEqual(len(response.json), 3)
