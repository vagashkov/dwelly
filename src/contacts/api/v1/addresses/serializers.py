from rest_framework.serializers import ModelSerializer

from django_countries.serializer_fields import CountryField

from ....models import CompanyAddress


class AddressSerializer(ModelSerializer):
    """
    Manages company address object details serialization
    """

    class Meta:
        model = CompanyAddress
        fields = [
            CompanyAddress.Field.country,
            CompanyAddress.Field.city,
            CompanyAddress.Field.street_address,
            CompanyAddress.Field.zip_code,
            ]

    country: CountryField = CountryField()
