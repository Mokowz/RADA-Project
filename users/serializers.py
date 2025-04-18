from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(">>> USING CUSTOM REGISTER SERIALIZER")
        self.fields.pop('username', None)


    def get_cleaned_data(self):
        return super().get_cleaned_data()
    
    def save(self, request):
        user = super().save(request)
        user.save()
        return user
