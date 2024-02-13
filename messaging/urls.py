# # messaging/urls.py
# from django.urls import path
# from .views import message_list, message_detail, user_messages
#
# urlpatterns = [
#     path('messages/', message_list, name='message-list'),
#     path('messages/<str:receiver>/', message_detail, name='message-detail'),
#     path('user-messages/', user_messages, name='user-messages'),
# ]





# messaging/urls.py
from django.urls import path
from .views import message_list, message_detail, user_messages, delete_message

urlpatterns = [
    path('messages/', message_list, name='message-list'),
    path('messages/<str:receiver>/', message_detail, name='message-detail'),
    path('messages/<int:message_id>/delete/', delete_message, name='delete-message'),
    path('user-messages/', user_messages, name='user-messages'),
]
