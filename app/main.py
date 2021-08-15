import os
from typing import (
    List,
    Optional,
)

from jinja2 import (
    Environment,
    FileSystemLoader,
)
from pydantic import ValidationError
from sqlalchemy.orm import Session
from werkzeug.exceptions import (
    HTTPException,
    NotFound,
)
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import (
    Map,
    Rule,
)
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.wrappers import (
    Request,
    Response,
)

from app import (
    schemas,
    models,
)
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.repository import (
    get_comment_sqlalchemy_repository,
    get_post_sqlalchemy_repository,
)


class BulletinBoard:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
        self.url_map = Map(
            [
                Rule("/", endpoint="posts"),
                Rule("/create_post", endpoint="create_post"),
                Rule("/<id>", endpoint="post_detail"),
                Rule("/<post_id>/create_comment", endpoint="create_comment"),
            ]
        )

        # init database
        self.session: Session = SessionLocal()

        self.post_repository = get_post_sqlalchemy_repository(
            session=self.session
        )
        self.comment_repository = get_comment_sqlalchemy_repository(
            session=self.session
        )

    # Close database session on application shutdown.
    def __del__(self):
        self.session.close()

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype="text/html")

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f"on_{endpoint}")(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    # Endpoints

    def on_posts(self, request):
        posts: List[
            models.Post
        ] = self.post_repository.get_posts_order_by_date()

        return self.render_template("index.html", posts=posts)

    def on_create_post(self, request):
        error: Optional[str] = None

        if request.method == "POST":
            try:
                post_create: schemas.PostCreate = schemas.PostCreate(
                    **request.form
                )

                self.post_repository.create(obj_in=post_create)

                return redirect("/")
            except ValidationError as exception:
                error = exception.json()

        return self.render_template("create_post.html", error=error)

    def on_post_detail(self, request, id: int):
        post: Optional[models.Post] = self.post_repository.get_with_comments(
            id=id
        )

        if post is None:
            raise NotFound()

        return self.render_template("post_detail.html", post=post)

    def on_create_comment(self, request, post_id: int):
        error: Optional[str] = None

        if request.method == "POST":
            try:
                comment_create: schemas.CommentCreate = schemas.CommentCreate(
                    **request.form, post_id=post_id
                )

                self.comment_repository.create(obj_in=comment_create)

                return redirect(f"/{post_id}")
            except ValidationError as exception:
                error = exception.json()

        return self.render_template("create_comment.html", error=error)


def create_app(with_static=True):
    app = BulletinBoard()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app,
            {"/static": os.path.join(os.path.dirname(__file__), "static")},
        )
    return app


if __name__ == "__main__":
    init_db()

    app = create_app()
    run_simple(
        settings.HOSTNAME,
        settings.SERVER_PORT,
        app,
        use_debugger=settings.DEBUG,
    )
