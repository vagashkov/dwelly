from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings

from core.models import Reference
from listings.models import Listing, PriceTag, Reservation
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
    Listing.Field.check_in_time: "14:00",
    Listing.Field.check_out_time: "12:00",
    Listing.Field.instant_booking: True
}

good_price_tag = {
    PriceTag.Field.start_date: date.today(),
    PriceTag.Field.end_date: date.today() + relativedelta(months=1),
    PriceTag.Field.price: 100,
    PriceTag.Field.description: "Test price tag description"
}

good_reservation = {
    Reservation.Field.check_in: date.today(),
    Reservation.Field.check_out: date.today() + relativedelta(weeks=1),
    Reservation.Field.comment: "Test reservation comment"
}
