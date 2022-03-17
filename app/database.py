from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/post'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind =engine)

Base= declarative_base()

# dependency

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
 # cursor.execute("""INSERT INTO post (title, content, published) 
    # VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    # created = cursor.fetchone()

    # conn.commit()
    # print(current_user.id)
    #created = models.Post(title = post.title, content = post.content, published = post.published)
# cursor.execute("""INSERT INTO post (title, content, published) 
    # VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    # created = cursor.fetchone()

    # conn.commit()
    # print(current_user.id)
    #created = models.Post(title = post.title, content = post.content, published = post.published)
# def find_index_id(id):
#     for i, p in enumerate(my_post):
#         if p["id"] == id:
#          return i

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p



# @app.get("/post/latest")
# def get_latest():
#    post =  my_post[len(my_post)-1]
#    return {"details": post}
 # post = find_post(int(id))

    # cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with Id {id} was not found")
    #     # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with Id {id} was not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"post with Id {id} was not found"}
# cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # # index = find_index_id(int(id))
# cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    # (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()

    # conn.commit() 



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='post', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('db connection success')
#         break
#     except Exception as e:
#         print('db connection failed')

# my_post  = [{"title": "first post", "content": "this is the first post on this site", "id": 1},
#  {"title": "second poat", "content": "this is the second post on thi site", "id":2}]


# @app.get('/sqlalchemy')
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"data": posts} 