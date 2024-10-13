from sqladmin import ModelView

from apps.models.models import Category, Product, User


class UserAdmin(ModelView, model=User):
    column = [User.name, User.username, User.description]
    can_view_details = False

class ProductAdmin(ModelView, model=Product):
    column = [Category.id, Category.name]


class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    form_rules = ['name', ]
    can_export = False
