from users.models import User, Profile

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
