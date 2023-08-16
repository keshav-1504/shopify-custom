import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def product_delete(request):
    print("==============")
    print("Product Deteleted...")
    print("REQUEST: ", request.GET)
    print("REQUEST POST: ", request.POST)
    print("REQUEST BODY: ",  json.loads(request.body))
    print("==============")

    return JsonResponse({'msg': "Succcess", "status": True})


@csrf_exempt
def order_fulfilled(request):
    print("Order/Fulfillment Webhook Triggered >>> Data Rcvd..")
    print("==============\n")
    fulfilledItem = json.loads(request.body)
    print(fulfilledItem)
    # for items in fulfilledItem['line_items']:
    #     print(f"Fulfilled {items['name']}")
    print("\n==============")

    return JsonResponse({'msg': "Succcess", "status": True})
