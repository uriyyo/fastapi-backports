from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from fastapi_backports import APIRouter, FastAPI

app = FastAPI()


@app.get("/", middleware=[Middleware(CORSMiddleware)])
async def app_get() -> None:
    pass


@app.post("/", middleware=[Middleware(CORSMiddleware)])
async def app_post() -> None:
    pass


@app.patch("/", middleware=[Middleware(CORSMiddleware)])
async def app_patch() -> None:
    pass


@app.put("/", middleware=[Middleware(CORSMiddleware)])
async def app_put() -> None:
    pass


@app.delete("/", middleware=[Middleware(CORSMiddleware)])
async def app_delete() -> None:
    pass


@app.options("/", middleware=[Middleware(CORSMiddleware)])
async def app_options() -> None:
    pass


@app.head("/", middleware=[Middleware(CORSMiddleware)])
async def app_head() -> None:
    pass


@app.trace("/", middleware=[Middleware(CORSMiddleware)])
async def app_trace() -> None:
    pass


@app.websocket("/", middleware=[Middleware(CORSMiddleware)])
async def app_websocket() -> None:
    pass


@app.api_route("/", methods=["GET", "POST"], middleware=[Middleware(CORSMiddleware)])
async def app_api_route() -> None:
    pass


app.add_api_route(
    "/",
    app_api_route,
    methods=["GET", "POST"],
    middleware=[Middleware(CORSMiddleware)],
)

app.add_api_websocket_route(
    "/",
    app_websocket,
    middleware=[Middleware(CORSMiddleware)],
)

router = APIRouter(middleware=[Middleware(CORSMiddleware)])


@router.get("/", middleware=[Middleware(CORSMiddleware)])
async def router_get() -> None:
    pass


@router.post("/", middleware=[Middleware(CORSMiddleware)])
async def router_post() -> None:
    pass


@router.patch("/", middleware=[Middleware(CORSMiddleware)])
async def router_patch() -> None:
    pass


@router.put("/", middleware=[Middleware(CORSMiddleware)])
async def router_put() -> None:
    pass


@router.delete("/", middleware=[Middleware(CORSMiddleware)])
async def router_delete() -> None:
    pass


@router.options("/", middleware=[Middleware(CORSMiddleware)])
async def router_options() -> None:
    pass


@router.head("/", middleware=[Middleware(CORSMiddleware)])
async def router_head() -> None:
    pass


@router.trace("/", middleware=[Middleware(CORSMiddleware)])
async def router_trace() -> None:
    pass


@router.websocket("/", middleware=[Middleware(CORSMiddleware)])
async def router_websocket() -> None:
    pass


@router.api_route("/", methods=["GET", "POST"], middleware=[Middleware(CORSMiddleware)])
async def router_api_route() -> None:
    pass


router.add_api_route(
    "/",
    router_api_route,
    methods=["GET", "POST"],
    middleware=[Middleware(CORSMiddleware)],
)

router.add_api_websocket_route(
    "/",
    app_websocket,
    middleware=[Middleware(CORSMiddleware)],
)

second_router = APIRouter(middleware=[Middleware(CORSMiddleware)])
router.include_router(second_router, middleware=[Middleware(CORSMiddleware)])
app.include_router(router, middleware=[Middleware(CORSMiddleware)])
