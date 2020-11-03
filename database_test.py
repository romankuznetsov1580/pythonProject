import asyncio
import aiopg

dsn = 'dbname=rainbow_database user=unicorn_user password=magical_password host=0.0.0.0 port=5430'

async def go():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * from posts")
                ret = []
                async for row in cur:
                    ret.append(row)
                    print(row)
                # assert ret == [(1,)]

loop = asyncio.get_event_loop()
loop.run_until_complete(go())
