from properties.models import PropertyChat, PropertyChatMessage


def get_chat_recipients(chat_id: int) -> list[str]:
    chat = PropertyChat.objects.get(id=chat_id)
    return [chat.client.id, chat.property.listed_by.user.id]


def get_chat_message_recipients(chat_message_id: int) -> list[str]:
    chat_message = PropertyChatMessage.objects.get(id=chat_message_id)
    return [chat_message.chat.client.id, chat_message.chat.property.listed_by.user.id]
