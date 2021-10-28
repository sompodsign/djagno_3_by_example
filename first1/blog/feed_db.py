
import uuid
from django.contrib.auth.models import User
from blog.models import Post


for _ in range(100):
    user = User.objects.create_user(username='john',
                                    email=f'{str(uuid.uuid4())[:10]}@gmail.com',
                                    password='5946644S')
    post = Post(author=User, title=f'Test post {str(uuid.uuid4())}',
                body=f'Body Text {str(uuid.uuid4())}',
                status='published')
    post.save()




