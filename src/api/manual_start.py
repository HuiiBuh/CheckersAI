import uvicorn


def manual_start_app(location='main:app', reload: bool = True):
    uvicorn.run(location, port=1234)


if __name__ == '__main__':
    manual_start_app()
