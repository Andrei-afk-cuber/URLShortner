from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, Response

from .cache_utills import lifespan
from .crud import create_link, get_link_by_code, update_clicks
from .database import session_dep
from .schemas import LinkBase, LinkPublic

app = FastAPI(lifespan=lifespan)


# Health check path
@app.get("/health")
async def health():
    return {"status": "ok"}


# Validate URL and generate code
@app.post("/shorten", response_class=Response)
async def code_generation(link: LinkBase, session: session_dep):
    link_orm = await create_link(session, link)
    return Response(content=link_orm.code, status_code=201)


# Redirect and counter increment
@app.get("/{code}")
async def code(request: Request, code: str, session: session_dep):
    # Try to get cache
    redis_client = request.app.state.redis

    link_id, link_url = await redis_client.hmget(f"link:{code}", ["id", "original_url"])

    if link_id and link_url:
        await update_clicks(session, link_id=int(link_id))
        return RedirectResponse(link_url)

    # Get data from db and set cache
    link = await get_link_by_code(session, code)

    await redis_client.hset(f"link:{code}", mapping=jsonable_encoder(link))
    await redis_client.expire(f"link:{code}", 300)
    await update_clicks(session, link_id=link.id)

    return RedirectResponse(url=link.original_url, status_code=307)


# Getting code stats
@app.get("/stats/{code}", response_model=LinkPublic)
async def stats(request: Request, code: str, session: session_dep):
    # Get data from cache
    redis_client = request.app.state.redis

    link_data = await redis_client.hgetall(f"link:{code}")

    if link_data:
        link = LinkPublic(**link_data)
    else:
        # Get data from database
        link = await get_link_by_code(session, code)

        await redis_client.hset(f"link:{code}", mapping=jsonable_encoder(link))
        await redis_client.expire(f"link:{code}", 300)

    return link
