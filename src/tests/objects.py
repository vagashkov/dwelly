from os import mkdir
from os.path import exists

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify

from listings.models import (
    ObjectType, Category, Amenity, HouseRule,
    Listing, Photo
)
from users.models import User

from .data import (
    object_type, category, amenities_list, house_rules_list,
    good_user, good_listing, TEST_DIR
)


def create_good_user() -> User:
    # create new user
    return User.objects.create_user(
        email=good_user.get(
            User.Field.email
        ),
        password=good_user.get(
            User.Field.password
        )
    )


def upload_cover(listing: Listing) -> None:
    # prepare test image to upload
    image = Image.new(
        "RGB",
        size=(2000, 2000),
        color=(155, 0, 0)
    )

    if not exists(TEST_DIR):
        mkdir(TEST_DIR)

    image_path = TEST_DIR / "test_photo.jpg"
    image.save(image_path)

    cover_photo = Photo(
        index=0,
        title="Test cover photo",
        listing=listing,
        is_cover=True
    )

    # "upload" post cover
    with open(image_path, "rb") as profile_photo:
        cover_photo.file = SimpleUploadedFile(
            name="post_cover.jpg",
            content=profile_photo.read(),
            content_type="image/jpeg"
        )

    cover_photo.save()


def create_good_listing() -> Listing:
    # Object type
    apartments = ObjectType.objects.create(
        **object_type
    )

    # Amenities (essential and not)
    essentials = Category.objects.create(
        **category
    )

    amenities = list()
    for amenity in amenities_list:
        amenities.append(
            Amenity.objects.create(
                **amenity,
                category=essentials
            )
        )

    # House rules
    house_rules = list()
    for house_rule in house_rules_list:
        house_rules.append(
            HouseRule.objects.create(
                **house_rule
            )
        )

    # Create test listing
    listing = Listing.objects.create(
        **good_listing,
        slug=slugify(
            good_listing.get(
                Listing.Field.title
            )
        ),
        object_type=apartments
    )
    listing.amenities.set(amenities)
    listing.house_rules.set(house_rules)
    listing.save()

    upload_cover(listing)

    return listing
