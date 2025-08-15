from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from core.models import Reference

from ....models import HouseRule
from .permissions import HouseRulePermissions
from .serializers import HouseRuleSerializer


class HouseRules(ListCreateAPIView):
    """
    Manages house rule listing and new house rule creation
    """

    queryset = HouseRule.objects.all()
    serializer_class = HouseRuleSerializer
    pagination_class = None
    permission_classes = [HouseRulePermissions]


class HouseRuleDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single house rule instance lifecycle
    """

    queryset = HouseRule.objects.all()
    lookup_field = Reference.Field.name
    lookup_url_kwarg = Reference.Field.name
    serializer_class = HouseRuleSerializer
    permission_classes = [HouseRulePermissions]
