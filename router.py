from importlib import import_module
from pathlib import Path

from fastapi import APIRouter

from fapix.core.homepage import router as _fapix_homepage_router
from apps.auth.urls import router as auth_router
from apps.courses.urls import router as courses_router
from apps.assessments.urls import router as assessments_router
from apps.communications.urls import router as communications_router

router = APIRouter()
router.include_router(_fapix_homepage_router)







router.include_router(auth_router)

router.include_router(courses_router)

router.include_router(assessments_router)

router.include_router(communications_router)
