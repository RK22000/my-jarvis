from fastapi import FastAPI
from .auth import router as auth_router, MIDDLEWARE_KEY
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=MIDDLEWARE_KEY)
app.include_router(auth_router)

@app.get("/health")
def health():
    return "OK"