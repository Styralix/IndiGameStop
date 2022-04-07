from django.core.exceptions import ValidationError
from django.test import TestCase

from IndiDevStop.accounts.models import Profile


class ProfileTests(TestCase):
    VALID_USER_DATA = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male',
    }

    def test_profile_create_when_first_name_only_letters__expect_success(self):
        profile = Profile(**self.VALID_USER_DATA)

        self.assertEqual(profile.first_name, self.VALID_USER_DATA['first_name'])

    def test_profile_create_when_first_name_contains_digits__expect_to_fail(self):
        profile = Profile(
            first_name='John1',
            last_name='Doe',
            username='johndoe',
            email='testmail@abv.bg',
            profile_picture='12.jpg',
            gender='Male'
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_first_name_contains_symbols__expect_to_fail(self):
        profile = Profile(
            first_name='John$&',
            last_name='Doe',
            username='johndoe',
            email='testmail@abv.bg',
            profile_picture='12.jpg',
            gender='Male'
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_first_name_is_empty__expect_to_fail(self):
        profile = Profile(
            first_name='',
            last_name='Doe',
            username='johndoe',
            email='testmail@abv.bg',
            profile_picture='12.jpg',
            gender='Male'
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_last_name_contains_symbols__expect_to_fail(self):
        profile = Profile(
            first_name='John',
            last_name='Doe$%^',
            username='johndoe',
            email='testmail@abv.bg',
            profile_picture='12.jpg',
            gender='Male'
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_last_name_is_empty__expect_to_fail(self):
        profile = Profile(
            first_name='John',
            last_name='',
            username='johndoe',
            email='testmail@abv.bg',
            profile_picture='12.jpg',
            gender='Male'
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_last_name_contains_space__expect_fail(self):
        profile = Profile(
            first_name='John',
            last_name='Doe e',
            username='johndoe',
            email='testmail@abv.bg',
            profile_picture='12.jpg',
            gender='Male'
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_username__when_valid_expect_correct_username(self):
        profile = Profile(**self.VALID_USER_DATA)

        self.assertEqual(profile.username, self.VALID_USER_DATA['username'])
