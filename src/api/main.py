from fastapi import FastAPI

from api.AuthenticationMiddleware import AuthenticationMiddleware
from api.endpoints import game

# auth_token = os.environ.get('auth_token')
auth_token = "123456789"

app = FastAPI()
app.include_router(game.router)
app = AuthenticationMiddleware(app, auth_token)
