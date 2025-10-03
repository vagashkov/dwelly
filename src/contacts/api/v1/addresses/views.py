from django.db.utils import IntegrityError

from pyngo import drf_error_details

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.views import APIView

from ....constants import ERROR_KEY
from ....models import Company, CompanyAddress

from .permissions import AddressPermissions
from .serializers import AddressSerializer
from .validators import AddressValidator


class CreateAddress(APIView):
    """
    Manages company object lifecycle
    """

    model = CompanyAddress
    serializer_class = AddressSerializer
    permission_classes = [AddressPermissions]

    def post(self, request: Request) -> Response:
        """
        New address creation routine
        :param request:
        :return:
        """

        if not Company.objects.count():
            raise NotFound

        # First, validate data using pydantic class
        try:
            AddressValidator.model_validate(
                    request.data
                    )
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: drf_error_details(error)
                }
            )

        # Deserialize and check data
        serializer = AddressSerializer(data=request.data)
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
            address = serializer.save(
                company=Company.objects.all()[0]
            )
        except IntegrityError as e:
            return Response(
                data={ERROR_KEY: e},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        # And return result
        return Response(
            data=AddressSerializer(address).data,
            status=HTTP_201_CREATED
        )

    def get(self, request: Request) -> Response:
        """
        Company address getting routine
        :param request:
        :return:
        """

        if not self.model.objects.count():
            raise NotFound

        return Response(
            status=HTTP_200_OK,
            data=AddressSerializer(
                self.model.objects.all()[0]
                ).data
            )

    def patch(self, request: Request) -> Response:
        """
        Company address editing routine
        :param request:
        :return:
        """

        if not self.model.objects.count():
            raise NotFound

        if not Company.objects.count():
            raise NotFound

        # First, validate data using pydantic class
        try:
            AddressValidator.model_validate(
                    request.data
                    )
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: drf_error_details(error)
                }
            )

        # Deserialize and check data
        serializer = AddressSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: error.detail
                }
            )

        address = CompanyAddress.objects.all()[0]

        for key, value in request.data.items():
            address.__setattr__(
                key, value
            )

        try:
            address.save()
        except IntegrityError as e:
            return Response(
                data={ERROR_KEY: e},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        # And return result
        return Response(
            data=AddressSerializer(address).data,
            status=HTTP_200_OK
        )

    def delete(self, request: Request) -> Response:
        """
        Company address deletion routine
        :param request:
        :return:
        """

        if not self.model.objects.count():
            raise NotFound

        self.model.objects.all()[0].delete()

        # And return result
        return Response(
            status=HTTP_204_NO_CONTENT
        )
