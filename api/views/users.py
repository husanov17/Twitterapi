from rest_framework.views import APIView
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema

from api.utils import send_code_to_email
from api.serializers import EmailSerializer, CodeSerializer, FullSignUpSerializer, LoginSerializer
from api.models import User, CODE_VERIFIED, DONE
from rest_framework.permissions import IsAuthenticated
from api.utils import CustomResponse


@extend_schema(tags=['Auth'])
class SendEmailRegistrationAPIView(APIView):
    serializer_class = EmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.create(
            email=email
        )
        send_code_to_email(email, user.create_verify_code())

        return CustomResponse.success(
            status=True,
            message="Confirmation code has sent to you email.",
            data=user.token()
        )
    

@extend_schema(tags=['Auth'])
class CodeVerifyAPIView(APIView):
    serializer_class = CodeSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        if self.verify_code(user, code):
            return CustomResponse.success(
                status=True,
                message="Code verified successfully",
                data=user.token()
            )

        return CustomResponse.error(
            status=False,
            message="Code don't match or code expired"
        )

    def verify_code(self, user: User, code: int):
        confirmation = user.confirmations.order_by("-created_at").first()
        if confirmation.code == code and confirmation.is_expired():
            user.status = CODE_VERIFIED
            user.save()
            return True
        

@extend_schema(tags=['Auth'])
class ResendCodeAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        confirmation = user.confirmations.order_by("-created_at").first()

        if confirmation.is_expired():
            return CustomResponse.error(
                status=False,
                message="Code has not been expired"
            )
    
        send_code_to_email(user.email, user.create_verify_code())

        return CustomResponse.success(
            status=True,
            message="Confirmation code has sent to your email.",
            data=user.token()
        )
        

@extend_schema(tags=['Auth'])   
class FullSignUpAPIView(APIView):
    serializer_class = FullSignUpSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        if user.status not in [CODE_VERIFIED, DONE]:
            return CustomResponse.error(
                status=False,
                message="You are not verified."
            )
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.status = DONE
        user.save()

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": user.email
        }

        return CustomResponse.success(
            status=True,
            message="User has been registered successfully",
            data=data
        )


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        seralizer = self.serializer_class(data=request.data)
        seralizer.is_valid(raise_exception=True)

        username = seralizer.validated_data.get('username')
        password = seralizer.validated_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return CustomResponse.success(
                status=True,
                message="You logged in successfully.",
                data=user.token()
            )

        return CustomResponse.success(
            status=False,
            message="Username or email or password invalid"
            )



        
        


        
