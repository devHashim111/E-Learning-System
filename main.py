from fastapi import FastAPI

from router import router
from contextlib import asynccontextmanager
from db_config import TORTOISE_ORM, connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
# @app.on_event("startup")
# async def seed_default_rooms():
#     room_names = ["General Chat", "Support"]
#     for name in room_names:
#         room, created = await ChatRoom.get_or_create(name=name)
#         print(f"Room: '{room.name}' | ID: {room.id}")
from fastapi.middleware.cors import CORSMiddleware



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins for production
    allow_credentials=True,
    allow_methods=["*"],  # Explicitly allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)