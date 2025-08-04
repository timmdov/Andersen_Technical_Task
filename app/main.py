from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="ToDo API", version="1.0.0",)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )