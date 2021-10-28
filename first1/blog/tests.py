from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User


# Create your tests here.
class PostTestCase(TestCase):

    def test_post_detail(self):
        test1 = Post.objects.get(id=3)
        print(test1)
        self.assertEqual(test1.body, 'Body text alskjdfalksjdf;alksdjf;alsd a lot of text.')
