from rest_framework.serializers import ModelSerializer

from ...models import Company


class CompanySerializer(ModelSerializer):
    """
    Manages blog object details serialization
    """

    class Meta:
        model = Company
        fields = [
            Company.Field.full_name,
            Company.Field.short_name,
            Company.Field.license,
            Company.Field.registration,
            ]
