from properties.models import PropertyChat, PropertyChatMessage
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def get_chat_recipients(chat_id: int) -> list[str]:
    chat = PropertyChat.objects.get(id=chat_id)
    # All admin id
    admins = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).values_list(
        "id", flat=True
    )
    return list(set([chat.client.id, chat.property.listed_by.user.id] + list(admins)))


def get_chat_message_recipients(chat_message_id: int) -> list[str]:
    chat_message = PropertyChatMessage.objects.get(id=chat_message_id)
    admins = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).values_list(
        "id", flat=True
    )
    return list(
        set(
            [chat_message.chat.client.id, chat_message.chat.property.listed_by.user.id]
            + list(admins)
        )
    )
