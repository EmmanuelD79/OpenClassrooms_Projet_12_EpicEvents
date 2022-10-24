from django.contrib.auth import authenticate, login
from rest_framework import status, response
from utils.utils import get_tokens_for_user
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes



@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request):
    if 'email' not in request.data or 'password' not in request.data:
        return response.Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        tokens = get_tokens_for_user(request.user)
        return response.Response({'msg': 'Login Success', **tokens}, status=status.HTTP_200_OK)
    return response.Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        