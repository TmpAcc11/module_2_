import json

from config import GET_POSTS_DATA, GET_POSTS_DATA_SINGLE

from json import JSONDecodeError


def get_posts_all(path):
    """
    Post loader
    :param path: str, path to json file
    :return: list of dicts
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except JSONDecodeError:
        return []
    else:
        return data


def get_posts_by_user(user_name, posts):
    """
    Returns all posts by username
    :param posts: str, path to json
    :param user_name: str
    :return: list of dicts
    """
    posts_of_user = list()
    for post in posts:
        if post.get('poster_name', None) == str(user_name):
            posts_of_user.append(post)
    return posts_of_user


def get_comments_by_post_id(post_id, path):
    """
    Returns all comments by post id
    :param post_id: int
    :param path: str, path to json file
    :return: list of dicts
    """
    if not isinstance(post_id, int):
        raise TypeError('Invalid post_id type')
    comments_in_post = list()
    with open(path, 'r', encoding='utf-8') as file:
        comments = json.load(file)
    for comment in comments:
        if post_id == comment.get('post_id', None):
            comments_in_post.append(comment)
    if len(comments_in_post) == 0:
        return 'Схоже, що такого поста не існує'
    return comments_in_post


def search_for_posts(query, posts):
    """
    Returns all posts by query
    :param posts: str, path to json
    :param query: str
    :return: list of dicts
    """
    if not isinstance(query, str):
        raise TypeError('Invalid querry type.')
    search_posts = list()
    for post in posts:
        if query.lower() in post.get('content', None).lower():
            search_posts.append(post)
    if len(search_posts) == 0:
        return 'Нічого не знайдено'  # Це убога строка кода, має вертати None і це потім буде оброблятися у views
    return search_posts


def get_post_by_pk(pk, posts):
    """
    Returns one post by pk
    :param posts: str, path to jspn
    :param pk: int
    :return: dict
    """
    if not isinstance(pk, int):
        raise TypeError('Invalid pk type')
    for post in posts:
        if pk == post.get('pk', None):
            return post
    return dict()


def data_json_dump(data):
    """
    Writes data to a json file.
    :param data: dict or list
    :return: json
    """
    path = None
    if isinstance(data, list):
        path = GET_POSTS_DATA
    elif isinstance(data, dict):
        path = GET_POSTS_DATA_SINGLE
    data = json.dumps(data, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(data)


def tag_check(content):
    """
    Finds tags in text and adds hyperlinks to them/ Returns the updated post text
    :param content: str
    :return: str
    """
    if not isinstance(content, str):
        raise TypeError('Invalid content type')
    content_splited = content.split()
    for word in content_splited:
        if word.startswith('#'):
            word_with_tag = f'<a href="/tag/{word[1:]}" class="item__tag">{word}</a>'
            content_splited[content_splited.index(word)] = word_with_tag
    content = ' '.join(content_splited)
    return content


def get_bookmarks(path):
    """
    JSON loader. Returns list with post ids.
    :param path: str, path to json
    :return: list
    """
    with open(path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except JSONDecodeError:
            return []
        return data


def add_bookmark(postid, bookmarks, path):
    """
    Adds post id to the JSON
    :param postid: int(str)
    :param bookmarks: list
    :param path: str, path to JSON
    :return: None
    """
    postid = int(postid)
    with open(path, 'w', encoding='utf-8') as file:
        if postid not in bookmarks:
            bookmarks.append(postid)
        file.write(str(bookmarks))


def remove_bookmark(postid, bookmarks, path):
    """
    Removes post id from the JSON
    :param postid: int(str)
    :param bookmarks: list
    :param path: str, path to JSON
    :return: None
    """
    postid = int(postid)
    with open(path, 'w', encoding='utf-8') as file:
        bookmarks.remove(postid)
        file.write(str(bookmarks))
