from django.conf.urls import url, include
from django.urls import path
from chat.views import LogIn,LogOut,GetMessages,SendMessage,HomeView,GetOnlineUsersView


urlpatterns = [
    path('',HomeView.as_view()),
    path('login/', LogIn.as_view()),
    path('logout/', LogOut.as_view()),
    path('get-online-users/',GetOnlineUsersView.as_view()),
    path('get-messages/<user_id>/',GetMessages.as_view()),
    path('send-message/<session_uuid>/',SendMessage.as_view()),

]