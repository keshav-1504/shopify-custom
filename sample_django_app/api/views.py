import requests
from django.http import JsonResponse
from shopify_app.decorators import session_token_required
from django.views.decorators.csrf import csrf_exempt
import shopify
import base64


@session_token_required
def products(request):
    products = shopify.Product.find()
    return JsonResponse({'products': [p.to_dict() for p in products]})


@session_token_required
def orders(request):
    orders = shopify.Order.find(status='any')
    return JsonResponse({'orders': [o.to_dict() for o in orders]})

# ++++=====================================================++++ >> KJ
@csrf_exempt
@session_token_required
def addProduct(request):
    print("Adding Products...")
    print("Image: ", request.FILES.get("productImage"))
    productName = request.POST.get("productName")
    productImage = request.FILES.get("productImage")
    productPrice = request.POST.get("productPrice")
    productQuantity = request.POST.get("productQuantity")
    productDescription = request.POST.get("productDescription")
    print("Image type: ", type(productImage))
    print(f'Name {productName} Image {productImage} Price {productPrice} Quantity {productQuantity} Description {productDescription}')
    status = True
    try:
        product = shopify.Product()
        image = shopify.Image()

        product.title = productName
        product.tags = "camera,dslr,nikon"
        variants = []
        variantData = {}
        variantData['title'] = "Variant Title"
        variantData['price'] = productPrice
        variantData['inventory_quantity'] = productQuantity
        variants.append(variantData)
        product.body_html = productDescription
        product.variants = variants
        product.product_type = "Camera"
        product.save()
        image.product_id = product.id
        image.position = 1
        image.attachment = base64.b64encode(
            productImage.read()).decode("utf-8")
        image.filename = "test.jpg"
        image.save()

        print("Inventory ID: ", product.variants[0].inventory_item_id)

    except Exception as e:
        status = False
        print("Error : ", e)
    return JsonResponse({'msg': "Succcess", "status": status})


@csrf_exempt
@session_token_required
def updateInventory(request, *args, **kwargs):
    inventory_id = request.POST.get("inventory_id")
    productCost = request.POST.get("productCost")
    productQuantity = request.POST.get("productQuantity")
    print(str(inventory_id))
    inventory = shopify.InventoryItem.find_first(ids=str(inventory_id))
    inventory.cost = productCost
    inventory.tracked = True
    inventory.inventory_quantity = productQuantity
    inventory.save()

    print(f"{inventory_id} {productCost} {productQuantity}")
    return JsonResponse({'msg': "Succcess", "status": True})


@csrf_exempt
@session_token_required
# No other method is working. use this method to create/update* metafield of Products.
def addProductMetafield(request, *args, **kwargs):
    # print(kwargs)
    productId = request.POST.get("owner_id")
    # print("product id", productId)
    shopify_domain = kwargs['shopify_domain']
    access_token = kwargs['access_token']

    response = createMetaField(createMetaFieldFor="products",
                               shopifyDomain=shopify_domain, accessToken=access_token, id=productId)

    print("RESPONSE: >> : ", response)

    return JsonResponse({'msg': "Succcess", "status": True})


@csrf_exempt
@session_token_required
# No other method is working. use this method to create/update* metafield of Orders. - KJ
def addOrderMetafield(request, *args, **kwargs):
    # print(kwargs)
    orderId = request.POST.get("orderId")
    print("orderId", orderId)
    shopify_domain = kwargs['shopify_domain']
    access_token = kwargs['access_token']

    response = createMetaField(createMetaFieldFor="orders",
                               shopifyDomain=shopify_domain, accessToken=access_token, id=orderId)

    print("RESPONSE: >> : ", response)

    return JsonResponse({'msg': "Succcess", "status": True})


def createMetaField(createMetaFieldFor, shopifyDomain, accessToken, id):
    headers = {
        'X-Shopify-Access-Token': accessToken,
        'Content-Type': 'application/json',
    }

    json_data = {
        'metafield': {
            'namespace': 'product',
            'key': f'my_custom_key_for_{createMetaFieldFor}',
            'value': 49000,
            'type': 'number_integer',
        },
    }

    response = requests.post(
        f'https://{shopifyDomain}/admin/api/2023-07/{createMetaFieldFor}/{id}/metafields.json',
        headers=headers,
        json=json_data,
    )
    return response.text


@csrf_exempt
@session_token_required
def createOrder(request, *args, **kwargs):
    title = request.POST.get("title")
    price = request.POST.get("price")
    quantity = request.POST.get("quantity")
    print(f"Title: {title} price: {price} quantity: {quantity}")
    order = shopify.Order()
    items = {"title": title,
             "price": price,
             "quantity": quantity}
    line_items = [items]
    order.line_items = line_items
    order.save()

    print("ORDER: ", order)

    return JsonResponse({'msg': "Succcess", "status": True})


# ---------------IMPORTANT--------------
# This is the only working method for fulfilling orders.
# 1. Get fulfillment_order_id using FulfillmentOrders by passing order ID.
# 2. Create Json Data and make a POST request to the specified URL. [shopify Classes not working] - KJ


@csrf_exempt
@session_token_required
def orderFulfillment(request, *args, **kwargs):
    orderId = request.POST.get("orderId")
    shopify_domain = kwargs['shopify_domain']
    access_token = kwargs['access_token']

    fo = shopify.FulfillmentOrders.find(order_id=orderId)[0]

    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json',
    }

    json_data = {
        'fulfillment': {
            'line_items_by_fulfillment_order': [
                {
                    'fulfillment_order_id': fo.id,
                },
            ],
            'tracking_info': {
                'number': 'MS1562678',
                'url': 'https://www.my-shipping-company.com?tracking_number=MS1562678',
                'company': 'keshavbits',
            },
        },
    }

    response = requests.post(
        f'https://{shopify_domain}/admin/api/2023-07/fulfillments.json',
        headers=headers,
        json=json_data,
    )

    print(response.text)

    # return response.text
    return JsonResponse({'msg': "Succcess", "status": True})

# ++++=====================================================++++ >> KJ