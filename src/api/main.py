import os

from fastapi import FastAPI

from api.AuthenticationMiddleware import AuthenticationMiddleware
from api.endpoints import game

app = FastAPI()
app.include_router(game.router)

auth_token = os.environ.get('auth_token', '123456789')
app = AuthenticationMiddleware(app, auth_token)
