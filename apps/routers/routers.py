from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from apps.models.products import Product

templates = Jinja2Templates(directory="templates/apps/products")
product_router = APIRouter(prefix='/products')

# products = [
#     {   'id': 1,
#         'name': 'tote bag',
#         'price': 35
#      },
#     {
#         'id': 2,
#         'name': 'hobo bag',
#         'price': 66
#     },
#     {
#         'id': 3,
#         'name': 'leather jacket',
#         'price': 135
#     }
# ]


@product_router.get("/", name='products-list')
async def get_all_products(request: Request, session: AsyncSession):
    products = await Product.get_all(session)
    context = {
        'products': products
    }
    return templates.TemplateResponse(request, 'product-list.html', context)


@product_router.get(f"/detail/{id}", name='products-detail')
async def read_item(request: Request, item_id: id):
    product = await Product.get_by_id(item_id)
    context = {
        'product': product
    }
    return templates.TemplateResponse(request, 'product-detailb.html', context)



# @product_router.post('/')
# async def read_item(request: Request):
#     data = await request.form
#     await Product.create(**data)
#     return RedirectResponse('/products')

