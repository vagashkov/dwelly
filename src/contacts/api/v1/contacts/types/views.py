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

from core.models import Reference
from core.api.paginators import BasePaginator

from .....constants import ERROR_KEY
from .....models import ContactType

from .permissions import ContactsTypePermissions
from .serializers import ContactTypeSerializer
from .validators import ContactTypeValidator


class ContactTypes(ListCreateAPIView):
    """
    Manages company contact types lifecycle
    """

    model = ContactType
    pagination_class = BasePaginator
    serializer_class = ContactTypeSerializer
    permission_classes = [ContactsTypePermissions]

    def get_queryset(self):
        return ContactType.objects.all().order_by(Reference.Field.name)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        New contact type creation routine
        :param request:
        :return:
        """

        # First, validate data using pydantic class
        try:
            ContactTypeValidator.model_validate(
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
        serializer = ContactTypeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: error.detail
                }
            )

        # Try to create company object
        try:
            contact_type = serializer.save()
        except IntegrityError as e:
            return Response(
                data={ERROR_KEY: e},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        # And return result
        return Response(
            data=ContactTypeSerializer(contact_type).data,
            status=HTTP_201_CREATED
        )


class ContactTypeDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single contact type instance lifecycle
    """

    queryset = ContactType.objects.all()
    lookup_field = ContactType.Field.name
    lookup_url_kwarg = ContactType.Field.name
    serializer_class = ContactTypeSerializer
    permission_classes = [ContactsTypePermissions]
