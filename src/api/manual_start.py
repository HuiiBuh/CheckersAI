import uvicorn


def manual_start_app(location='main:app', reload: bool = False):
    uvicorn.run(location, port=1234, reload=reload)


if __name__ == '__main__':
    manual_start_app(reload=True)
