from django.conf import settings

from core.models import Reference
from listings.models import Listing
from users.models import User, Profile

TEST_DIR = settings.BASE_DIR / "test_data"

good_user = {
    User.Field.email: "test@email.com",
    User.Field.password: "S0meStr0ngPaSSw0rd",
}

good_profile = {
    Profile.Field.first_name: "Test",
    Profile.Field.last_name: "User",
    Profile.Field.phone: "+302374071345",
    Profile.Field.bio: "Some test user"
}

object_type = {
    Reference.Field.name: "Apartments",
    Reference.Field.description: "Comfortable and with fair price"
}

category = {
    Reference.Field.name: "Essentials",
    Reference.Field.description: "Mandatory for every living area"
}

amenities_list = [
    {
        Reference.Field.name: "Electricity",
        Reference.Field.description: "For light and appliances"
    },
    {
        Reference.Field.name: "Water",
        Reference.Field.description: "For drinking and washing",
    },
    {
        Reference.Field.name: "Central heating",
        Reference.Field.description: "Only for cold countries",
    },
    {
        Reference.Field.name: "Cooler",
        Reference.Field.description: "Only for hot countries"
    }
]

house_rules_list = [
    {
        Reference.Field.name: "No smoking",
        Reference.Field.description: "Healthy lifestyle preferred"
    },
    {
        Reference.Field.name: "Pets allowed",
        Reference.Field.description: "Pets are our family members",
    }
]

good_listing = {
    Listing.Field.title: "First listing",
    Listing.Field.description: "First test listing",
    Listing.Field.max_guests: 2,
    Listing.Field.beds: 1,
    Listing.Field.bedrooms: 1,
    Listing.Field.bathrooms: 1,
    Listing.Field.instant_booking: True
}
