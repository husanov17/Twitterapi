from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import send_code_to_email
from api.serializer import EmailSerializer
from api.models import User 

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

        data = {
            "status": True,
            "message": "Confirmation code has sent to you email.",
            "token": user.token()
        }
        return Response(data)
