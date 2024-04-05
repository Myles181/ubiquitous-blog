from .models import (User, Profile, Post, PostComment,  PostLike, PostDislike, 
                     CommentReply, CommentLike, CommentDislike)
from .serializers import (RegisterSerializer, MyTokenObtainPairSerializer, ProfileSerializer,
                          PostSerializer, PostCommentSerializer, PostLikeSerializer, PostDislikeSerializer,
                          CommentReplySerializer, CommentLikeSerializer, CommentDislikeSerializer)

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView



#Token Data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = TokenAuthentication



@api_view(['GET'])
def get_routes(request):
    routes = [
        'token/',
        'token/refresh/',
        'get_routes/',
        'profile/<int:id>',
        'update_profile/<int:id>',
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def protected_routes(request):
    if request.method == 'GET':
        return Response("Get request", )
    elif request.method == 'POST':
        return Response({"message": request.data.get("content")}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request, user_id):
    user = request.user
    if user_id is not user.id:
        return Response("You are not allowed in this endpoint", "Check your user id")
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request, user_id):
    user = request.user
    if user_id is not user.id:
        return Response("You are not allowed in this endpoint", "Check your user id")
    request.data['updated_at'] = timezone.now()
    serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['GET'])
def getPost_all(request):
    query_set = Post.objects.all()
    if not query_set:
        return Response({"message": "No posts"})

    # Initialize an empty list to store the post data
    posts_data = []

    # Iterate over each post in the query_set
    for post in query_set:
        # Extract the desired fields from each post
        username = post.author.username # Assuming 'author' is a ForeignKey to a User model
        title = post.title
        created_at = post.created_at

        # Append the extracted data to the list
        posts_data.append({
            "author": username,
            "title": title,
            "created_at": created_at
        })

    # Return the list of posts data as a response
    return Response({"posts": posts_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPost_by_id(request, user_id):
    user = request.user
    posts_data = []

    user_id = int(user_id)

    if user_id != user.id:
        return Response("You are not allowed in this endpoint", "Check your user id")
    author = request.user
    query_set = Post.objects.filter(author=author)
    # print([i for i in query_set])

    for query in query_set:
        title = query.title
        body = query.body
        cover_image = query.cover_image.url if query.cover_image else None
        created_at = query.created_at

        posts_data.append({"title": title,
                          "body": body,
                          "cover_image": cover_image,
                          "created_at": created_at
                })
    return Response({"posts": posts_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    validated_data = PostSerializer(data=request.data, context={'request': request})

    if validated_data.is_valid():
        validated_data.save()
        print(validated_data)
        return  Response({"message": validated_data.data['title']}, status=status.HTTP_201_CREATED)
    
    return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editPost(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    print(post)
    if not post:
        print(post)
        return Response({"message": "Invalid post id"})
    
    request.data['author'] = user
    request.data['updated_at'] = timezone.now()
    
    validated_data = PostSerializer(instance=post, data=request.data, partial=True)
    print(validated_data)
    if validated_data.is_valid():
        validated_data.save()
        return Response({"message": validated_data.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delPost(request, post_id):
    # Retrieve the post by its ID
    post = Post.objects.filter(id=post_id)

    if not post:
        return Response({"message": "Invalid post id"})
    # Delete the post
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostComments(request, post_id):
    post = Post.objects.get(id=post_id)
    if not post:
        return Response({"message": "Invalid Post Id"})
    
    query_set = PostComment.objects.filter(post=post)

    return Response(query_set, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPostComment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"message": "post id is Invalid"}, status=status.HTTP_404_NOT_FOUND)
    
    request.data['post'] = post.id
    request.data['author'] = request.user.id

    serializer = PostCommentSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        # Ensure the serializer's save method correctly handles the author and post fields
        serializer.save()
        return Response({"message": f"Success {serializer.data['body']}"}, status=status.HTTP_200_OK)

    return Response({"message": "Data not Validated", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editPostComment(request, comment_id):
    try:
        comment = PostComment.objects.get(id=comment_id, author=request.user)
    except PostComment.DoesNotExist:
        return Response({"message": "Comment not found or not authorized to edit"}, status=status.HTTP_404_NOT_FOUND)

    request.data['post'] = comment.post.author.id
    request.data['author'] = request.user.id

    serializer = PostCommentSerializer(instance=comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data.body, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePostComment(request, comment_id):
    try:
        comment = PostComment.objects.get(id=comment_id, author=request.user)
    except PostComment.DoesNotExist:
        return Response({"message": "Comment not found or not authorized to delete"}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)

def createCommentReply(request, comment_id):
    # Check if comment actually exists
    comment_author = get_object_or_404(PostComment, comment_id=comment_id)
    if not comment_author:
        return Response({"message": "post id is Invalid"})

    request.data['comment_author'] = comment_author
    request.data['author'] = request.user

    validated_data = CommentReplySerializer(data=request.data)

    if validated_data.is_valid():
        validated_data.save()

        return Response({"message": f"Success {validated_data.data['body']}"}, status=status.HTTP_200_OK)

    return Response({"meesage": "Data not Validated"}, status=status.HTTP_400_BAD_REQUEST)



def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    request.data['author'] = request.user
    request.data['post'] = post

    post_dislike = get_object_or_404(PostDislike, post=post)
    if post_dislike:
        post_dislike.delete()
        post_like = PostLikeSerializer(data=request.data)
        if post_like.is_valid():
            post_like.save()
            return Response({'message': 'success but post_dislike was deleted'}, status=status.HTTP_200_OK)
    else:
        post_like = PostLikeSerializer(data=request.data)
        if post_like.is_valid():
            post_like.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
    return Response({'message': 'failed. Post like was not saved :('}, status=status.HTTP_400_BAD_REQUEST)


def dislike_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    request.data['author'] = request.user
    request.data['post'] = post

    post_like = get_object_or_404(PostLike, post=post)
    if post_like:
        post_like.delete()
        post_dislike = PostDislikeSerializer(data=request.data)
        if post_dislike.is_valid():
            post_dislike.save()
            return Response({'message': 'success but post_like was deleted'}, status=status.HTTP_200_OK)
    else:
        post_dislike = PostDislikeSerializer(data=request.data)
        if post_dislike.is_valid():
            post_dislike.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
    return Response({'message': 'failed. Post dislike was not saved :('}, status=status.HTTP_400_BAD_REQUEST)


def like_comment(request, comment_id):
    try:
        comment = PostComment.objects.get(id=comment_id)
    except PostComment.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    request.data['author'] = request.user
    request.data['post'] = comment

    comment_dislike = get_object_or_404(CommentDislike, post=comment)
    if comment_dislike:
        comment_dislike.delete()
        comment_like = CommentLikeSerializer(data=request.data)
        if comment_like.is_valid():
            comment_dislike.save()
            return Response({'message': 'success but comment_dislike was deleted'}, status=status.HTTP_200_OK)
    else:
        comment_like = CommentLikeSerializer(data=request.data)
        if comment_like.is_valid():
            comment_like.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        
    return Response({'message': 'failed. Comment like was not saved :('}, status=status.HTTP_400_BAD_REQUEST)

def dislike_comment(request, comment_id):
    try:
        comment = PostComment.objects.get(id=comment_id)
    except PostComment.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    request.data['author'] = request.user
    request.data['post'] = comment

    comment_like = get_object_or_404(CommentLike, post=comment)
    if comment_like:
        comment_like.delete()
        comment_dislike = CommentDislikeSerializer(data=request.data)
        if comment_dislike.is_valid():
            comment_dislike.save()
            return Response({'message': 'success but comment_like was deleted'}, status=status.HTTP_200_OK)
    else:
        comment_dislike = CommentDislikeSerializer(data=request.data)
        if comment_dislike.is_valid():
            comment_dislike.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        
    return Response({'message': 'failed. Post like was not saved :('}, status=status.HTTP_400_BAD_REQUEST)



# def search_posts(request):