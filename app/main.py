from fastapi import FastAPI, WebSocket
from app.database import Base, engine
from app.routes import auth, projects, tasks
from app.websocket import connect, disconnect, notify_all

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Do nothing
    except:
        disconnect(websocket)
