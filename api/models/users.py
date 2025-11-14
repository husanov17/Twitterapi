from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import random
import uuid

NEW, CODE_VERIFILED, DONE = ('new', 'code_verifiled', 'done')


class User(AbstractUser):
    status_choices = (
        (NEW, NEW),
        (CODE_VERIFILED, CODE_VERIFILED),
        (DONE, DONE)
    )
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default=NEW)
    image = models.ImageField(upload_to="user_images/", validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    
    
    def __str__(self):
        return self.username
    
    def create_verify_code(self):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code
        )
        return code

    def save(self, *args, **kwargs):
        if not self.username:
            username = f"username-{uuid.uuid4()}"
            self.username = username

        if not self.password:
            password = f"password-{uuid.uuid4()}"
            self.password = password
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)


    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "accsess": str(refresh.access_token),
            "refresh": str(refresh)
        }
    
class UserConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmations")
    code = models.PositiveIntegerField()
    expire_time = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.expire_time = timezone.now()+timezone.timedelta(minutes=2)
        return super().save(*args, **kwargs)

    def is_expired(self):
        if self.expire_time > timezone.now():
            return False
        return True
    
    def __str__(self):
       return f"self.user.username | {self.code}"