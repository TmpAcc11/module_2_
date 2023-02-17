import pytest

from config import POSTS_PATH, COMMENTS_PATH, BOOKMARKS_PATH
from tests.conftest import posts
from utils import get_posts_all, get_posts_by_user, get_comments_by_post_id, search_for_posts, get_post_by_pk, \
    tag_check, get_bookmarks


class TestGetPostsAll(object):
    def test_get_posts_all_type(self):
        assert isinstance(get_posts_all(POSTS_PATH), list) == True, 'Отримана невірна структура даних'

    def test_get_posts_all_structure(self):
        excepted_keys = {
            'poster_name',
            'poster_avatar',
            'pic',
            'content',
            'views_count',
            'likes_count',
            'pk'
        }
        assert excepted_keys == set(get_posts_all(POSTS_PATH)[0].keys()), 'Дані отримані невірно'

    def test_get_posts_all_decode_error(self, path):
        assert get_posts_all(path[0]) == [], 'В разі JSONDecodeError має вертати пустий список'

    def test_get_posts_all_file_not_exist(self, path):
        with pytest.raises(FileNotFoundError):
            assert get_posts_all(path[2]) == path[3], 'Має зупиняти програму, якщо файл з постами не знайдений'


class TestGetPostsByUser(object):
    parameters_by_user = [('leo', {1, 5}), ('larry', {4, 8}), ('hank', {3, 7})]

    @pytest.mark.parametrize('poster_name, post_pks_correct', parameters_by_user)
    def test_get_posts_by_user_name_normal(self, posts, poster_name, post_pks_correct):
        user_posts = get_posts_by_user(poster_name, posts)
        posts_pks = set()
        for post in user_posts:
            posts_pks.add(post['pk'])
        assert posts_pks == post_pks_correct, 'Пошук по ніку користувача працює невірно'

    def test_get_posts_by_user_name_not_exist(self, posts):
        assert get_posts_by_user('Eren', posts) == [], 'Неправильно опрацьовує випадок з неіснуючим користувачем'


class TestGetCommentsByPostId(object):
    comments_by_post_id_params = [1, 2, 3, 4, 5]

    @pytest.mark.parametrize('post_id', comments_by_post_id_params)
    def test_get_comments_by_post_id_type(self, post_id):
        assert isinstance(get_comments_by_post_id(post_id, COMMENTS_PATH),
                          list) == True, 'Вертає невірну структуру даних'

    def test_get_posts_all_structure(self):
        excepted_keys = {
            'post_id',
            'commenter_name',
            'comment',
            'pk'
        }
        assert set(get_comments_by_post_id(1, COMMENTS_PATH)[0].keys()) == excepted_keys, 'Дані отримані невірно'

    comments_parameters_ids = [1, 2, 3, 4]

    @pytest.mark.parametrize('post_id', comments_parameters_ids)
    def test_get_comments_by_post_id_check_type(self, post_id):
        comments_for_post = get_comments_by_post_id(post_id, COMMENTS_PATH)
        for comment in comments_for_post:
            assert comment['post_id'] == post_id


class TestSearchForPost(object):
    post_parameters_search = [("тарелка", {1}), ("елки", {3}), ("проснулся", {4})]

    @pytest.mark.parametrize("query, post_pks_correct", post_parameters_search)
    def test_search_for_posts(self, posts, query, post_pks_correct):
        posts = search_for_posts(query, posts)
        post_pks = set()
        for post in posts:
            post_pks.add(post["pk"])
        assert post_pks == post_pks_correct


class TestPostByPk(object):
    parameters_get_by_pk = [(1, 'leo'), (2, 'johnny'), (3, 'hank'), (4, 'larry')]

    @pytest.mark.parametrize('post_pk, correct_poster_name', parameters_get_by_pk)
    def test_get_by_pk_check_format_and_keys(self, posts, post_pk, correct_poster_name):
        post_poster_name = get_post_by_pk(post_pk, posts)['poster_name']
        assert post_poster_name == correct_poster_name

    def test_get_by_pk_check_not_exist(self, posts):
        no_post = get_post_by_pk(0, posts)
        assert no_post == dict()


class TestTagCheck(object):
    def test_tag_check(self):
        assert tag_check(
            'Очень красивый #закат. Стоило выбраться из #дома, чтобы посмотреть на него! а где ты был?'
        ) == 'Очень красивый <a href="/tag/закат." class="item__tag">#закат.</a> Стоило выбраться из <a href="/tag/дома," class="item__tag">#дома,</a> чтобы посмотреть на него! а где ты был?'


class TestGetBookmarks(object):
    def test_get_bookmarks_type(self):
        assert isinstance(get_bookmarks(BOOKMARKS_PATH), list) == True, 'Невірна структура даних'
