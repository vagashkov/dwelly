from accounts.models import Account, Profile

good_account = {
    Account.Field.email: "newuser@email.com",
    Account.Field.password: "S0meStr0ngPaSSw0rd",
}

good_profile = {
    Profile.Field.first_name: "Some",
    Profile.Field.last_name: "User",
    Profile.Field.country: "GR",
    Profile.Field.phone: "+302374071345",
    Profile.Field.birth_date: "1970-08-25",
    Profile.Field.language: "el",
    Profile.Field.bio: "Some test user"
}
