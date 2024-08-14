from django.test import TestCase
from .models import Author, Post, Comment

class AuthorModelTest(TestCase):
    def setUp(self):
        Author.objects.create(name="John Doe", email="john@example.com", bio="A bio")

    def test_author_name(self):
        author = Author.objects.get(name="John Doe")
        self.assertEqual(author.name, "John Doe")

class PostModelTest(TestCase):
    def setUp(self):
        author = Author.objects.create(name="John Doe", email="john@example.com", bio="A bio")
        Post.objects.create(title="Sample Post", content="Some content", author=author)

    def test_post_title(self):
        post = Post.objects.get(title="Sample Post")
        self.assertEqual(post.title, "Sample Post")

class CommentModelTest(TestCase):
    def setUp(self):
        author = Author.objects.create(name="John Doe", email="john@example.com", bio="A bio")
        post = Post.objects.create(title="Sample Post", content="Some content", author=author)
        Comment.objects.create(content="A comment", post=post)

    def test_comment_content(self):
        comment = Comment.objects.get(content="A comment")
        self.assertEqual(comment.content, "A comment")
