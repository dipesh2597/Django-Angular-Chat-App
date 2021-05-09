from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from chat.models import ChatMessage,ChatSession
from chat.serializers import UserSerializer,ChatMessageSerializer
from django.db.models import Q
from channels import Channel,Group

class HomeView(APIView):
    def get(self,request):
        return Response({'message': "Welcome to my Chat App"}, status=HTTP_200_OK)


class LogIn(APIView):
    
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'message': 'Please provide both email and password'},status=HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            user=None
        if user:
            if user.check_password(password):
                try:
                    token, _ = Token.objects.get_or_create(user=user)
                except Exception as e:
                    pass
                
                user_data = UserSerializer(user).data
                return Response({'token': token.key,'user':user_data}, status=HTTP_200_OK)
            else:
                return Response({'message': 'Invalid Username or Password'}, status=HTTP_400_BAD_REQUEST)    
        else:
            return Response({'message': 'no user associated with this email please enter check email.'}, status=HTTP_400_BAD_REQUEST)

class GetOnlineUsersView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        online_users = Token.objects.exclude(user=request.user).values('user_id','user__first_name','user__last_name')
        return Response(online_users, status=HTTP_200_OK)

class LogOut(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # simply deleting the token to force a login
        try:
            Token.objects.get(user=request.user)
        except:
            return Response({"message":"User token not available"},status=HTTP_400_BAD_REQUEST)  
        request.user.auth_token.delete()
        return Response({"message":"User logged out successfully"},status=HTTP_200_OK)

class GetMessages(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,user_id):
        #fetching sessions started by both users
        first_user = request.user
        second_user = User.objects.get(id=user_id)
        chat_sessions=ChatSession.objects.filter(Q(first_user=first_user,second_user=second_user) | Q(first_user=second_user,second_user=first_user)).order_by('started_at')
        if not chat_sessions:
            chat_session = ChatSession.objects.create(first_user=request.user,second_user=second_user)
        elif chat_sessions.latest('started_at').ended_at:
            chat_session = ChatSession.objects.create(first_user=request.user,second_user=second_user)
        else:
            chat_session = chat_sessions.latest('started_at')
        chat_messages = ChatMessage.objects.filter(session__in=chat_sessions).order_by('sent_at')
        messages = ChatMessageSerializer(chat_messages,many=True,context={'user':request.user}).data
        data={'current_session_uuid':chat_session.session_uuid,'message':messages}
        return Response(data,status=HTTP_200_OK)

class SendMessage(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request,session_uuid):
        message = request.data.get('message')
        chat_session = ChatSession.objects.get(session_uuid=session_uuid)
        created_message=ChatMessage.objects.create(session=chat_session,message=message,from_user=request.user)
        Group("%s" % session_uuid).send({
            "text": ChatMessageSerializer(created_message).data,
        })
        return Response ({'session_uuid': chat_session.session_uuid, 'message': ChatMessageSerializer(created_message).data,},status=HTTP_200_OK)