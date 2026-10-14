from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_routers import router as auth_router
from app.routers.bussiness_routers import router as bussiness_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(bussiness_router)