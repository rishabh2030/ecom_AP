from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer
from helper.functions import *
from helper import keys,messages
from .models import User
class UserRegisterAPI(generics.CreateAPIView):
    """
    API endpoint for user registration.

    Inherits from generics.CreateAPIView to handle user creation.

    Uses UserRegisterSerializer for data serialization during registration.
    """
    serializer_class = UserRegisterSerializer
    def create(self, request, *args, **kwargs):
        """
        Handle user registration.

        :param request: The HTTP request object containing user registration data.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Response containing the result of the user registration.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            user = serializer.save()
            token, refresh_token = user.get_tokens()
            token = {"access_token": token,"refresh_token": refresh_token}
            return Response(ResponseHandling.success_response_message(messages.REGISTRACTION_USER, token), status=status200)
        except Exception as e:
            return Response(ResponseHandling.failure_response_message(messages.EMAIL_ALREADY_EXIST, messages.OPERATION_FAILED), status=status400)

class UserLoginAPI(generics.CreateAPIView):
    """
    API endpoint for user login.

    Inherits from generics.CreateAPIView to handle user login.

    Uses UserLoginSerializer for data serialization during login.
    """

    serializer_class = UserLoginSerializer
    def create(self, request, *args, **kwargs):
        """
        Handle user login.

        :param request: The HTTP request object containing user login data.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Response containing the result of the user login.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            
            if not serializer.is_valid(raise_exception=False):
                errors = serializer.errors
                err = error_message_function(errors)
                return Response(ResponseHandling.failure_response_message(err, messages.OPERATION_FAILED), status=status400)
            
            email = request.data[keys.EMAIL]
            password = request.data[keys.PASSWORD]
            if not email and password:
                return Response(ResponseHandling.failure_response_message(messages.PROVIDE_FIELDS, messages.OPERATION_FAILED), status=status400)
            
            user = UserFunctions.get_user(email)
            if not user.check_password(password):
                return Response(ResponseHandling.failure_response_message(messages.WRONG_PASSWORD, messages.OPERATION_FAILED),status=status400)
            
            token, refresh_token = user.get_tokens()
            
            token = {"access_token": token, "refresh_token": refresh_token}
            return Response(ResponseHandling.success_response_message(messages.LOGIN_SUCCESS, token), status=status200)
        except Exception as e:
            return Response(ResponseHandling.success_response_message(messages.SOMETHING_WRONG, messages.OPERATION_FAILED), status=status400)