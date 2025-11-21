from rest_framework.views import APIView
from api.utils import CustomResponse
from api.serializers import PostCreateSerializer, MediaSerializer
from api.permissions import IsAuthenticatedAndDone, IsAuthenticatedAndAutor, IsAuthenticatedAndAutorForMedia
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import Post, Media
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes



@extend_schema(tags=['Post'])
class CreatePostAPIView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedAndDone, ]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=user)

        return CustomResponse.success(
            status=True,
            message="Post created successfully",
            data=serializer.data
        )

@extend_schema(tags=['Post'])
class UpdateDeleteAPIView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedAndAutor, ]

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = self.serializer_class(post, data=request.data)
            serializer.is_valid(raise_exception=True)
        except:
            return CustomResponse.error(
                status=False,
                message="Post doesn't exist."
            )

        serializer.save()
        return CustomResponse.success(
            status=True,
            message="Post updated successfully.",
            data=serializer.data
        )

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
        except:
            return CustomResponse.error(
                status=False,
                message="Post doesn't exist."
            )

        return CustomResponse.success(
            status=True,
            message="Post deleted successfully."
        )
    

@extend_schema(tags=['Post'])
class CreateMediaAPIView(APIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedAndDone, ]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'post': {
                        'type': 'integer',
                    },
                    'media': {
                        'type': 'string',
                        'format': 'binary',
                    }
                }
            }
        },
        responses={200: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return CustomResponse.success(
            status=True,
            message="Media created successfully",
            data=serializer.data
        )
    

@extend_schema(tags=['Post'])
class DeleteMediaAPIView(APIView):
    permission_classes = [IsAuthenticatedAndAutorForMedia, ]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'pk': {
                        'type': 'integer',
                    }
                }
            }
        },
        responses={200: OpenApiTypes.OBJECT},
    )
    def delete(self, request, pk):
        try:
            media = Media.objects.get(pk=pk)
            media.delete()
        except:
            return CustomResponse.error(
                status=False,
                message="Media doesn't exist."
            )

        return CustomResponse.success(
            status=True,
            message="Media deleted successfully"
        )