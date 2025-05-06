from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm, UserCreationForm

from .models import CustomUser

class AdminCustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "profile_image")