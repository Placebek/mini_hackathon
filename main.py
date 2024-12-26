from fastapi import FastAPI
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.middleware.cors import CORSMiddleware
from app.router import route
from fastapi.responses import HTMLResponse


app = FastAPI()

app.include_router(route)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Apache Logs Stream</title>
    </head>
    <body>
        <h1>Apache Access Log</h1>
        <pre id="accessLog"></pre>
        <script src="/static/app.js"></script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)
