from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from IndiDevStop.accounts.models import Profile
from IndiDevStop.web.models import Game, Post

UserModel = get_user_model()


class HomeViewTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class AllGamesViewTests(TestCase):
    def test_all_games_page_status_code(self):
        response = self.client.get('/all/games/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('all games'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('all games'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_games.html')

    def test_view_uses_correct_template_with_games(self):
        game = Game(
            title='Doom',
            picture='12.jpg',
            description='bs',
            type='RPG',
            release_date='2022-12-12',
            download_link='https://www.google.com/',
        )

        response = self.client.get(reverse('all games'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_games.html')


class AllPostsViewTests(TestCase):
    def test_all_posts_page_status_code(self):
        response = self.client.get('/all/posts/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('all posts'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('all posts'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')

    def test_view_uses_correct_template_with_posts(self):
        post = Post(
            title='Doom',
            body='sadasdasd',
        )

        response = self.client.get(reverse('all posts'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')


class my_games_Tests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_GAME_DATA = {
        'title': 'Doom',
        'picture': '12.jpg',
        'description': 'asdasdadsasd',
        'type': 'RPG',
        'release_date': '2022-12-12',
        'download_link': 'https://www.google.com/',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_game_for_user(self, user):
        game = Game.objects.create(
            **self.VALID_GAME_DATA,
            user=user,
        )

        game.save()
        return game

    def test_my_games_page_status_code(self):
        response = self.client.get('/my/games/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('my games'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('my games'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_games.html')

    def test_when_user_has_no_games__games_should_be_empty(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        response = self.client.get('/my/games/')

        self.assertEqual(
            0,
            len(response.context['games'])
        )

    def test_when_user_has_1_game__games_should_be_1(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        game = self.__create_game_for_user(user)

        response = self.client.get('/my/games/')

        self.assertEqual(
            1,
            len(response.context['games'])
        )


class CreateGameViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_GAME_DATA = {
        'title': 'Doom',
        'picture': '12.jpg',
        'description': 'asdasdadsasd',
        'type': 'RPG',
        'release_date': '2022-12-12',
        'download_link': 'https://www.google.com/',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_game_for_user(self, user):
        game = Game.objects.create(
            **self.VALID_GAME_DATA,
            user=user,
        )

        game.save()
        return game

    def test_create_game_page_status_code_when_no_user(self):
        response = self.client.get('/add/game/')
        self.assertEquals(response.status_code, 302)

    def test_when_creating_a_game_invalid_data__expect_error(self):
        game_data = Game(
            title='',
            picture='12.jpg',
            description='asdasdadsasd',
            type='RPG',
            release_date='2022-12-12',
            download_link='https://www.google.com/',
        )

        with self.assertRaises(Exception) as context:
            game_data.save()

        self.assertIsNotNone(context.exception)

    def test_when_creating_a_game_valid_data__expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        game = self.__create_game_for_user(user)

        games = Game.objects.all()

        self.assertEqual(
            1,
            len(games)
        )


class CreatePostViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_POST_DATA = {
        'title': 'Doom',
        'body': 'asdlaksjfsdkjfhsdjklf',
    }

    INVALID_POST_DATA = {
        'title': '',
        'body': '',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_post_for_user(self, user):
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            user=user,
        )

        post.save()
        return post

    def test_create_post_page_status_code_when_no_user(self):
        response = self.client.get('/add/post/')
        self.assertEquals(response.status_code, 302)

    def test_when_creating_a_post_valid_data__expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        post = self.__create_post_for_user(user)

        posts = Post.objects.all()

        self.assertEqual(
            1,
            len(posts)
        )

    def test_when_creating_a_post_invalid_data__expect_error(self):
        post_data = Post(
            title='',
            body='',
        )

        with self.assertRaises(Exception) as context:
            post_data.save()

        self.assertIsNotNone(context.exception)


class EditGameViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_GAME_DATA = {
        'title': 'Doom',
        'picture': '12.jpg',
        'description': 'asdasdadsasd',
        'type': 'RPG',
        'release_date': '2022-12-12',
        'download_link': 'https://www.google.com/',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_game_for_user(self, user):
        game = Game.objects.create(
            **self.VALID_GAME_DATA,
            user=user,
        )

        game.save()
        return game

    def test_edit_game_expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        game = self.__create_game_for_user(user)

        response = self.client.post(reverse('edit game', kwargs={'pk': game.pk}))

        games = Game.objects.all()

        self.assertEqual(
            1,
            len(games)
        )


class DeleteGameViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_GAME_DATA = {
        'title': 'Doom',
        'picture': '12.jpg',
        'description': 'asdasdadsasd',
        'type': 'RPG',
        'release_date': '2022-12-12',
        'download_link': 'https://www.google.com/',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_game_for_user(self, user):
        game = Game.objects.create(
            **self.VALID_GAME_DATA,
            user=user,
        )

        game.save()
        return game

    def test_delete_existing_game_expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        game = self.__create_game_for_user(user)

        response = self.client.post(reverse('delete game', kwargs={'pk': game.pk}))

        games = Game.objects.all()

        self.assertEqual(
            0,
            len(games)
        )


class EditPostViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_POST_DATA = {
        'title': 'Doom',
        'body': 'asdasdfafdasdasd',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_game_for_user(self, user):
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            user=user,
        )

        post.save()
        return post

    def test_edit_post_expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        post = self.__create_game_for_user(user)

        response = self.client.post(reverse('edit post', kwargs={'pk': post.pk}))

        posts = Post.objects.all()

        self.assertEqual(
            1,
            len(posts)
        )

        self.assertEqual(200, response.status_code)


class DeletePostViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'email': 'testmail@abv.bg',
        'password': 'aklsdhjskj@324wses',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John1',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'testmail@abv.bg',
        'profile_picture': '12.jpg',
        'gender': 'Male'
    }

    VALID_POST_DATA = {
        'title': 'Doom',
        'body': 'asdlaksjfsdkjfhsdjklf',
    }

    INVALID_POST_DATA = {
        'title': '',
        'body': '',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_post_for_user(self, user):
        post = Post.objects.create(
            **self.VALID_POST_DATA,
            user=user,
        )

        post.save()
        return post

    def test_delete_post_expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        credentials = {
            'email': 'testmail@abv.bg',
            'password': 'aklsdhjskj@324wses',
        }

        self.client.login(**credentials)

        post = self.__create_post_for_user(user)

        response = self.client.post(reverse('delete post', kwargs={'pk': post.pk}))

        posts = Post.objects.all()

        self.assertEqual(
            0,
            len(posts)
        )
