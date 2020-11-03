from sanic import Sanic
from sanic.response import json, text

import asyncio
import aiopg

app = Sanic("App Name")

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/ping")
async def test1(request):
    return json({"hello": "ROMA"})

@app.route("/post/<post_num:int>", methods=['GET'])
async def test2(request, post_num):
    # if not isinstance(post_num, int):
    # if not post_num.isdigit():
    #     return text(body='post_num must be integer', status=400)
    #return json({"post_num - {}".format(post_num)})
    return json({"post number" : "{}".format(post_num)})

@app.route('/post', methods=['POST'])
async def post_handler(request):
    return text('POST request - {}'.format(request.json))

@app.route('/get', methods=['GET'])
async def get_handler(request):
    return json({'result': []})

@app.route('/posts/<post_id:int>', methods=['PUT'])
async def get_handler(request, post_id):
    return text('PUT request body - {}, post_id - {}'.format(request.body, post_id))

async def get_all_posts_from_db():
   connect_to_db_url = 'dbname=rainbow_database user=unicorn_user password=magical_password host=0.0.0.0 port=5430'
    #  открываем пул коннектов к базе
   async with aiopg.create_pool(connect_to_db_url) as pool:
       # забираем коннект из пула
       async with pool.acquire() as conn:
           # берём курсор - чтобы выополять запросы
           async with conn.cursor() as cur:
               await cur.execute("SELECT * from posts;")
               all_posts = []
               async for post in cur:
                   all_posts.append(post)
   return all_posts
   # возвращаем список постов

@app.route('/posts', methods=['GET'])
async def get_handler(request):
    all_posts = await get_all_posts_from_db()
    return json({'result': all_posts})


loop = asyncio.get_event_loop()
loop.run_until_complete(get_all_posts_from_db())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, auto_reload=True)

