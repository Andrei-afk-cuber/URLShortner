import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response

from .crud import create_link, get_link_by_code, update_clicks
from .database import session_dep
from .schemas import LinkBase, LinkPublic

app = FastAPI()


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
async def code(code: str, session: session_dep):
    link = await get_link_by_code(session, code)
    await update_clicks(session, link_id=link.id)
    return RedirectResponse(url=link.original_url, status_code=307)


# Getting code stats
@app.get("/stats/{code}", response_model=LinkPublic)
async def stats(code: str, session: session_dep):
    link = await get_link_by_code(session, code)
    return link


if __name__ == "__main__":
    uvicorn.run(app)
