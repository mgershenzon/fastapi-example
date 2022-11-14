from fastapi import APIRouter

from fastapi_example.api.routes import bad_route, health, info, post_example, root, sleep

router = APIRouter()
router.include_router(bad_route.router, tags=["bad_route"])
router.include_router(health.router, tags=["health"])
router.include_router(info.router, tags=["info"])
router.include_router(root.router, tags=["root"])
router.include_router(sleep.router, tags=["sleep"])
router.include_router(post_example.router, tags=["post_example"])
