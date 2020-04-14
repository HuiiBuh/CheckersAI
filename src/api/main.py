from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from api.endpoints import game

app = FastAPI()
token = '123456789'


# @app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if 'X-authentication-token' not in request.headers:
        exception: dict = {'error': 'No X-authentication-token header'}
        return JSONResponse({'detail': exception}, status_code=401)

    header_token = request.headers['X-authentication-token']

    if header_token != token:
        exception: dict = {'error': 'Wrong X-authentication-token'}
        return JSONResponse({'detail': exception}, status_code=401)

    return await call_next(request)


app.include_router(game.router)
