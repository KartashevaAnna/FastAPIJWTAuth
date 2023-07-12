import os
import bcrypt

from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import JWT_signature
from app.models import Post, User
from app.schema import PostSchema, UserInSchema, UserLoginSchema, UserOutSchema

load_dotenv(".env")

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

SALT = b"$2b$12$b6HezbZpslamxu5/wv8UU."


@app.get("/", tags=["root"])
def read_root() -> dict:
    return {"message": "Pong!"}


def check_user(data: UserLoginSchema):
    user = db.session.query(User).filter_by(email=data.email).one()
    hashed_password = str(bcrypt.hashpw(data.password.encode("utf-8"), SALT))
    if user.email == data.email and user.password == hashed_password:
        return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return JWT_signature(user.email)
    return {"error": "Wrong login details!"}


@app.post(
    "/user/signup", response_model=UserOutSchema, tags=["user"], summary="Add new user"
)
async def user(user: UserInSchema = Body(...)):
    try:
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), SALT)
        db_user = User(
            name=user.name,
            email=user.email,
            password=str(hashed_password),
        )
        db.session.add(db_user)
        db.session.commit()
        return db_user
    except Exception as error:
        return f"This email is already in use. Please, choose another."


"""!!!!!!!!! Delete before final push!!!!!!!"""


@app.get("/user/", tags=["user"], summary="show all users")
async def user():
    users = db.session.query(User).all()
    return users


@app.post("/users/", tags=["user"], summary="delete all users")
async def user():
    users = db.session.query(User).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return 200


@app.post(
    "/post",
    response_model=PostSchema,
    dependencies=[Depends(JWTBearer())],
    tags=["posts"],
    summary="Add a post",
)
async def add_post(post: PostSchema) -> dict:
    db_post = Post(title=post.title, content=post.content, author_id=post.author_id)
    db.session.add(db_post)
    db.session.commit()
    return db_post


@app.get(
    "/posts",
    dependencies=[Depends(JWTBearer())],
    tags=["posts"],
    summary="Show all posts",
)
async def book():
    posts = db.session.query(Post).all()
    return posts


@app.get("/post/{post_id}", tags=["posts"])
def show_post(post_id: int):
    db_post = db.session.query(Post).filter_by(id=post_id).one()
    print(db_post)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.post(
    "/post/{post_id}",
    dependencies=[Depends(JWTBearer())],
    tags=["posts"],
    summary="Delete a post",
)
async def remove_post(post_id):
    db_post = db.session.query(Post).filter_by(id=post_id).one()
    db.session.delete(db_post)
    db.session.commit()
    return 200


@app.patch(
    "/post/{post_id}",
    response_model=PostSchema,
    dependencies=[Depends(JWTBearer())],
    tags=["posts"],
    summary="Update a post",
)
def update_post(post_id: int, post_to_change: PostSchema):
    db_post = db.session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post_to_change.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    db.session.add(db_post)
    db.session.commit()
    db.session.refresh(db_post)
    return db_post
