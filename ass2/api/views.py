from django.views.generic import ListView, DetailView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, Post, Comment, Tag
from .serializers import CustomUserSerializer, PostSerializer, CommentSerializer, TagSerializer
from django.core.cache import cache

@api_view(['POST'])
def add_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_tag(request):
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def posts_view_level_cache(request):
    if request.method == 'GET':
        posts = Post.objects.prefetch_related('comments', 'tags').select_related('author')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def post_by_id_low_level(request, pk):
    if request.method == 'GET':
        comments_cache_key = f'comments_count_{pk}'
        comments_count = cache.get(comments_cache_key)

        if not comments_count:
            try:
                post = Post.objects.get(id=pk)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            comments_count = post.comments.count()
            cache.set(comments_cache_key, comments_count, timeout=20)

        post = Post.objects.prefetch_related('tags', 'author').get(id=pk)

        serializer = PostSerializer(post)
        serializer_data = serializer.data
        serializer_data['comments_count'] = comments_count

        return Response(serializer_data)

class PostListView(ListView):
    model = Post
    template_name = 'api/posts.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.prefetch_related('comments', 'tags').select_related('author')

class PostDetailView(DetailView):
    model = Post
    template_name = 'api/post_details.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.prefetch_related('comments', 'tags').select_related('author')

@api_view(['GET', 'POST'])
def posts(request):
    if request.method == 'GET':
        price_cache_name = 'posts_cache'
        cached_posts = cache.get(price_cache_name)

        if cached_posts:
            serializer_data = cached_posts
        else:
            posts = Post.objects.prefetch_related('comments', 'tags').select_related('author')
            serializer = PostSerializer(posts, many=True)
            serializer_data = serializer.data
            cache.set(price_cache_name, serializer_data, timeout=30)
        return Response(serializer_data)

    if request.method == 'POST':
        user_id = request.data.get('author')
        try:
            author = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def comments_by_post(request, post_id):
    if request.method == 'GET':
        print(post_id)
        comments = Comment.objects.filter(post_id=post_id).select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tags(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def add_comment(request):
    if request.method == 'POST':
        user_id = request.data.get('author')
        post_id = request.data.get('post')
        try:
            author = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, post=post)
            comments_cache_key = f'comments_count_{post_id}'
            cache.delete(comments_cache_key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
