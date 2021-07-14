from fastapi import APIRouter

from fastapi_example.api.routes import bad_route, health, info, root

router = APIRouter()
router.include_router(bad_route.router, tags=["bad_route"])
router.include_router(health.router, tags=["health"])
router.include_router(info.router, tags=["info"])
router.include_router(root.router, tags=["root"])
