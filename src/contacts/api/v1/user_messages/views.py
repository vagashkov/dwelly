from django.db.utils import IntegrityError

from pyngo import drf_error_details
from pydantic import ValidationError as PydanticError

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from core.models import BaseModel
from core.api.paginators import BasePaginator

from ....constants import ERROR_KEY
from ....models import Contact, ContactType

from .permissions import UserMessagePermissions
from .serializers import ContactSerializer
from .validators import ContactValidator


class ContactMessages(ListCreateAPIView):
    """
    Manages company contacts listing and creation
    """

    model = Contact
    pagination_class = BasePaginator
    serializer_class = ContactSerializer
    permission_classes = [UserMessagePermissions]

    def get_queryset(self):
        return Contact.objects.all().order_by(
            BaseModel.Field.created_at
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        New contact creation routine
        :param request:
        :return:
        """

        # First, validate data using pydantic class
        try:
            ContactValidator.model_validate(
                    request.data
                    )
        except PydanticError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: drf_error_details(error)
                }
            )

        # Deserialize and check data
        serializer = ContactSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: error.detail
                }
            )

        contact_type = ContactType.objects.get(
            id=request.data.get(Contact.Field.contact_type)
        )

        # Try to create contact object
        try:
            contact = serializer.save()
            contact.contact_type = contact_type
            contact.save()
        except IntegrityError as e:
            return Response(
                data={ERROR_KEY: e},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        # And return result
        return Response(
            data=ContactSerializer(contact).data,
            status=HTTP_201_CREATED
        )


class ContactMessageDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single contact type instance lifecycle
    """

    queryset = Contact.objects.all()
    lookup_field = BaseModel.Field.id
    serializer_class = ContactSerializer
    permission_classes = [UserMessagePermissions]
