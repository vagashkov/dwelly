from pydantic import ValidationError

from pyngo import drf_error_details

from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from rest_framework.views import APIView

from ...constants import ERROR_KEY, ERROR_NO_COMPANY_FULL_NAME
from ...models import Company

from .permissions import CompanyPermissions
from .serializers import CompanySerializer
from .validators import CompanyValidator


class CreateCompany(APIView):
    """
    Manages company object lifecycle
    """

    model = Company
    serializer_class = CompanySerializer
    permission_classes = [CompanyPermissions]

    def post(self, request: Request) -> Response:
        """
        Company creation routine
        :param request:
        :return:
        """

        # First, validate data using pydantic class
        try:
            CompanyValidator.model_validate(
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
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Try to create company object
        company = serializer.save()

        # And return result
        return Response(
            data=CompanySerializer(company).data,
            status=HTTP_201_CREATED
        )

    def get(self, request: Request) -> Response:
        """
        Company getting routine
        :param request:
        :return:
        """

        if not self.model.objects.count():
            raise NotFound

        return Response(
            status=HTTP_200_OK,
            data=CompanySerializer(
                self.model.objects.all()[0]
            ).data
        )

    def patch(self, request: Request) -> Response:
        """
        Company editing routine
        :param request:
        :return:
        """

        if (
            Company.Field.full_name in request.data
            ) and not (
            request.data.get(Company.Field.full_name)
        ):
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: ERROR_NO_COMPANY_FULL_NAME
                }
            )

        if not self.model.objects.count():
            raise NotFound

        company = self.model.objects.all()[0]

        for key, value in request.data.items():
            company.__setattr__(
                key, value
            )

        company.save()

        # And return result
        return Response(
            data=CompanySerializer(company).data,
            status=HTTP_200_OK
        )

    def delete(self, request: Request) -> Response:
        """
        Company deletion routine
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
