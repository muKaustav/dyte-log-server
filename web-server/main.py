from fastapi import FastAPI
from routes.logs import logs

app = FastAPI()

app.include_router(logs, tags=["logs"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
