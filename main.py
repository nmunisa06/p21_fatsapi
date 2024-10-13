
from fastapi import FastAPI
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from apps.models.db import db
from apps.admin import CategoryAdmin, ProductAdmin

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
db.init()
admin = Admin(app, db._engine)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)


@app.on_event("startup")
def on_startup():
    db.init()
    # db.create_all()


@app.on_event("shutdown")
def on_startup():
    pass
    # db.drop_all()
