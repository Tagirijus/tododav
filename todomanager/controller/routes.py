'''
The web routes for the todomanager website.
'''

from fastapi import FastAPI

# UNCOMMENT WHEN WEBSITE RENDERING IS NEEDED
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi import Request
# import os


app = FastAPI()

# UNCOMMENT WHEN WEBSITE RENDERING IS NEEDED
# template_path = os.path.join(os.path.dirname(__file__), '..', 'view', 'templates')
# templates = Jinja2Templates(directory=template_path)


@app.get("/")
def read_home():
    return {"Hello": "World"}


# UNCOMMENT WHEN WEBSITE RENDERING IS NEEDED
# @app.get("/echo", response_class=HTMLResponse)
# async def read_echo(request: Request, q: str | None = None):
#     return templates.TemplateResponse(
#         'home/home.get.j2',
#         {
#             'request': request,
#             'q': q
#         }
#     )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
