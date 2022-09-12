import tempfile
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse

from .models import Comment
from .forms import CommentForm
from blogs.models import Blog


class CommentTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='setUpUser@gmail.com',
            username='setUpUser',
            password='12345',
        )
        self.blog = Blog.objects.create(
            title='blogT',
            slug='blogS',
            content='blogC',
            cover=tempfile.NamedTemporaryFile(suffix='.jpg').name,
            status='p',
            author=self.user,
        )

    def test_comment_form_anonymous_user(self):
        invalid_form = CommentForm(user=AnonymousUser(), data={
            'text': 'text',
            'score': 5,
        })
        valid_form = CommentForm(user=AnonymousUser(), data={
            'name': 'comment',
            'email': 'comment@gmail.com',
            'text': 'comment',
            'score': 5,
        })

        self.assertFalse(invalid_form.is_valid())
        self.assertTrue(valid_form.is_valid())

    def test_comment_form_authenticated_user(self):
        form = CommentForm(user=self.user, data={
            'text': 'test',
            'score': 5,
        })
        self.assertTrue(form.is_valid())

    def test_comment_view(self):
        response = self.client.post(reverse('comments:create', args=(self.blog.slug,)), data={
            'name': 'comment',
            'email': 'comment@gmail.com',
            'text': 'comment',
            'score': 5,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.exists())
        self.assertTrue(self.blog.comments.count())

    def test_child_comment(self):
        parent_comment = Comment.objects.create(
            name='parent',
            email='parent@gmail.com',
            text='parent_comment',
            score=5,
            blog=self.blog,
        )
        self.client.post(reverse('comments:create', args=(self.blog.slug,)), data={
            'name': 'child',
            'email': 'child@gmail.com',
            'text': 'child_comment',
            'score': 5,
            'parent': parent_comment.id,
        })

        self.assertTrue(parent_comment.children.exists())

    def test_comment_template_without_comments(self):
        response = self.client.get(reverse('blogs:detail', args=(self.blog.slug,)))

        self.assertContains(response, 'نظر خود را بنویسید')
        self.assertContains(response, 'هیج نظری وجود ندارد')

    def test_comment_template_with_comments(self):
        comment = Comment.objects.create(
            name='comment',
            email='comment@gmail.com',
            text='comment',
            score=5,
            blog=self.blog,
        )
        response = self.client.get(reverse('blogs:detail', args=(self.blog.slug,)))

        self.assertNotContains(response, 'هیج نظری وجود ندارد')
        self.assertContains(response, comment.name)
        self.assertContains(response, comment.text)

    def test_active_comments_in_template(self):
        comment = Comment.objects.create(
            name='active',
            email='active@gmail.com',
            text='active_comment',
            score=5,
            blog=self.blog,
            is_active=True
        )
        response = self.client.get(reverse('blogs:detail', args=(self.blog.slug,)))

        self.assertContains(response, comment.name)
        self.assertContains(response, comment.text)
        self.assertNotContains(response, 'هیج نظری وجود ندارد')

    def test_inactive_comments_in_template(self):
        comment = Comment.objects.create(
            name='inactive',
            email='inactive@gmail.com',
            text='inactive_comment',
            score=5,
            blog=self.blog,
            is_active=False
        )
        response = self.client.get(reverse('blogs:detail', args=(self.blog.slug,)))

        self.assertNotContains(response, comment.name)
        self.assertNotContains(response, comment.text)
        self.assertContains(response, 'هیج نظری وجود ندارد')
