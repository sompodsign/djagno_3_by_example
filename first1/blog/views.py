from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post, Comment
from .forms import EmailPostForm, CommentForm


# Create your views here.
# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 3)  # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # if page is not a in teger deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # if page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts})
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # assign hte current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def post_share(request, post_id):
    # retrieve by post id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form field passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'sompod123@gmail.com', ['sompod123@gmail.com'])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
