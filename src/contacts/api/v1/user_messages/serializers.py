from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from core.models import BaseModel

from ....models import UserMessage


class UserMessageSerializer(ModelSerializer):
    """
    Manages user message object serialization
    """

    class Meta:
        model = UserMessage
        fields = [
            UserMessage.Field.author,
            UserMessage.Field.contact_type,
            UserMessage.Field.contact,
            UserMessage.Field.text
            ]
        read_only_fields = [
            BaseModel.Field.id
        ]

        contact_type: SerializerMethodField = SerializerMethodField()

        def get_contact_type(self, instance):
            return instance.contact_type.id
