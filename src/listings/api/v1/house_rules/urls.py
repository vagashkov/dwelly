from django.urls import path

from .views import HouseRules, HouseRuleDetails

urlpatterns = [
    path(
        "<str:name>",
        HouseRuleDetails.as_view(),
        name="api_house_rule_details"
    ),
    path(
        "",
        HouseRules.as_view(),
        name="api_house_rules"
    )
]
