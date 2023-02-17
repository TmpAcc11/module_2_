import logging

from flask import Flask, render_template, send_from_directory, request, redirect

from utils import get_posts_all, get_post_by_pk, get_comments_by_post_id, search_for_posts, get_posts_by_user, \
    data_json_dump, tag_check, get_bookmarks, add_bookmark, remove_bookmark

from logging.config import dictConfig

from config import BOOKMARKS_PATH, COMMENTS_PATH, POSTS_PATH


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
LOGGING_FILE = './logs/api.log'
POSTS = get_posts_all(POSTS_PATH)
BOOKMARKS = get_bookmarks(BOOKMARKS_PATH)[1:]

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": f"{LOGGING_FILE}",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["file"]},
    }
)

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.after_request
def log_after_request(response):
    logging.info(f'% {request.path} | {request.method} | {response.status} | {response.content_length} %')
    return response


@app.errorhandler(404)
def page_not_found(error):
    logging.warning('Користувач спробував перейти на неіснуючу сторінку, помилка 404')
    return '<h1> 404 </h1>', 404


@app.errorhandler(500)
def internal_error(error):
    logging.error('Сталася помилка на стороні сервера, код 500', exc_info=True)
    return '<h1> 500 </h1>', 500


@app.route("/uploads/<path:name>")
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route('/')
def page_index():
    app.logger.info('Викликана головна сторінка')
    return render_template('index.html', posts=POSTS, bookmarks_counter=len(BOOKMARKS))


@app.route('/posts/<int:postid>')
def page_post(postid):
    post = get_post_by_pk(postid, POSTS)
    content = tag_check(post['content'])
    comments = get_comments_by_post_id(postid, COMMENTS_PATH)
    logging.info(f'Викликана сторінка поста з id {postid}')
    return render_template('post.html', post=post, content=content, comments=comments, comments_count=len(comments))


@app.route('/search')
def page_search():
    s = request.args.get('s')
    posts = search_for_posts(s, POSTS)[:10]
    logging.info(f'Виконано пошук по ключовому слову "{s}"')
    return render_template('search.html', posts=posts, posts_count=len(posts))


@app.route('/users/<username>')
def page_user_feed(username):
    logging.info(f'Викликана сторінка користувача з нікнеймом {username}')
    return render_template('user_feed.html', posts=get_posts_by_user(username, POSTS))


@app.route('/tag/<tagname>')
def page_tag(tagname):
    logging.info(f'Вкикликаний пошук постів за тегом: "{tagname}".')
    return render_template('tag.html', posts=search_for_posts(tagname, POSTS), tagname=tagname)


@app.route('/bookmarks/add/<postid>')
def page_add_bookmark(postid):
    add_bookmark(postid, BOOKMARKS, BOOKMARKS_PATH)
    logging.info(f'Додана закладка з id {postid}')
    return redirect('/', code=302)


@app.route('/bookmarks/remove/<postid>')
def page_remove_bookmark(postid):
    remove_bookmark(postid, BOOKMARKS, BOOKMARKS_PATH)
    logging.info(f'Видалена закладка з id {postid}')
    return redirect('/', code=302)


@app.route('/bookmarks/')
def page_bookmarks():
    posts = [get_post_by_pk(int(postid), POSTS) for postid in BOOKMARKS]
    logging.info('Викликана сторінка закладок')
    return render_template('bookmarks.html', posts=posts)


@app.route('/api/posts/', methods=['GET'])
def get_data():
    data_json_dump(POSTS)
    logging.info('Виконане запаковування даних усіх постів.')
    return '<h1> Дані постів успішно завантажені </h1>'


@app.route('/api/posts/<int:post_id>/', methods=['GET'])
def get_data_single(post_id):
    data_json_dump(get_post_by_pk(post_id, POSTS))
    logging.info(f'Виконано запаковування поста з id {post_id}')
    return '<h1> Дані поста успішно завантажені </h1>'


if __name__ == '__main__':
    app.run(debug=True)
