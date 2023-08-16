from django.shortcuts import render
from django.apps import apps
from django.views.decorators.clickjacking import xframe_options_exempt
from shopify_app.decorators import known_shop_required, latest_access_scopes_required

import shopify

from shopify_app.models import Shop


# ++++=====================================================++++ >> KJ

@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def index(request, *args, **kwargs):
    context = {
        "shop_origin": kwargs.get("shopify_domain"),
        "api_key": apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
        "scope_changes_required": kwargs.get("scope_changes_required"),
       
    }
    print("CONTEXT IN HOME: ",context)
    return render(request, "home/index.html", context)


# https://cdn.jsdelivr.net/npm/@shopify/polaris@11.11.0/build/esm/components/  -- USED THIS VERSION OF POLARIS
 
@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def products(request,*args, **kwargs): 
    try:
        shop_obj=Shop.objects.get(shopify_domain=kwargs.get("shopify_domain"))
        session = shopify.Session(shop_url=request.GET.get('shop'), version="2023-01",token=shop_obj.shopify_token)
        shopify.ShopifyResource.activate_session(session)
        products = shopify.Product.find()

        context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain"),
                "products":products}
        shopify.ShopifyResource.clear_session()

        return render(request,"home/products.html",context)
    except Exception as e:
        print("Error :",e)
        
    
@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def orders(request,*args, **kwargs):
    shop_obj=Shop.objects.get(shopify_domain=kwargs.get("shopify_domain"))
    session = shopify.Session(shop_url=request.GET.get('shop'), version="2023-01",token=shop_obj.shopify_token)
    shopify.ShopifyResource.activate_session(session)

    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
              "shop_origin": kwargs.get("shopify_domain"),}

    return render(request,"home/index.html",context)



def test(request):
    return render(request,"home/index.html")


@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def addProduct(request,*args, **kwargs):
    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain")}
    
    return render(request,'home/addProduct.html',context)

@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def updateInventory(request,*args, **kwargs):
    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain")}
    
    return render(request,'home/updateInventory.html',context)

@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def addProductMetafield(request,*args, **kwargs):
    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain")}
    
    return render(request,'home/addProductMetafield.html',context)


@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def addOrderMetafield(request,*args, **kwargs):
    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain")}
    
    return render(request,'home/addOrderMetafield.html',context)


@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def createOrder(request,*args, **kwargs):
    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain")}
    
    return render(request,'home/createOrder.html',context)



@xframe_options_exempt
@known_shop_required
@latest_access_scopes_required
def orderFulfillment(request,*args, **kwargs):
    context={"api_key":apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                "shop_origin": kwargs.get("shopify_domain")}
    
    return render(request,'home/orderFulfillment.html',context)

# ++++=====================================================++++ >> KJ