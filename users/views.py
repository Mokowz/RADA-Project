from dj_rest_auth.registration.views import RegisterView
from users.serializers import CustomRegisterSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer  # <- THIS is the fix

    def get_serializer_class(self):
        print(">>> USING CUSTOM REGISTER VIEW")
        return self.serializer_class