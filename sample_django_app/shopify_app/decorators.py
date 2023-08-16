from django.apps import apps
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect
from shopify import ApiAccess, Session, session_token
from shopify_app.models import Shop
from shopify_app.views import get_sanitized_shop_param


HTTP_AUTHORIZATION_HEADER = "HTTP_AUTHORIZATION"


def session_token_required(func):
    def wrapper(*args, **kwargs):

        try:
            decoded_session_token = session_token.decode_from_header(
                authorization_header=authorization_header(args[0]),
                api_key=apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
                secret=apps.get_app_config("shopify_app").SHOPIFY_API_SECRET,
            )
            # Added Manually to put and get data in kwargs which will be used in api views - KJ
            with shopify_session(decoded_session_token)[0]:
                kwargs = shopify_session(decoded_session_token)[1]
                return func(*args, **kwargs)
        except session_token.SessionTokenError:
            return HttpResponse(status=401)

    return wrapper


def shopify_session(session_token, *args, **kwargs):
    shopify_domain = session_token.get("dest").removeprefix("https://")
    api_version = apps.get_app_config("shopify_app").SHOPIFY_API_VERSION
    access_token = Shop.objects.get(
        shopify_domain=shopify_domain).shopify_token

    # Adding access_token and shopify_token for accessing it in api views - KJ
    kwargs['access_token'] = access_token
    kwargs['shopify_domain'] = shopify_domain
    return (Session.temp(shopify_domain, api_version, access_token), kwargs)


def authorization_header(request):
    return request.META.get(HTTP_AUTHORIZATION_HEADER)


def known_shop_required(func):
    def wrapper(*args, **kwargs):
        print("Args in wrapper is:", args)
        try:
            request = args[1]
        except:
            request = args[0]  # Added this, it will be used for function based views - KJ
        try:
            check_shop_domain(request, kwargs)
            check_shop_known(request, kwargs)

            return func(*args, **kwargs)
        except:
            print("\n===unable to get shop data.. returning to login.===\n")
            return redirect(reverse("login"))

    return wrapper


def check_shop_domain(request, kwargs):
    kwargs["shopify_domain"] = get_sanitized_shop_param(request)


def check_shop_known(request, kwargs):
    kwargs["shop"] = Shop.objects.get(
        shopify_domain=kwargs.get("shopify_domain"))


def latest_access_scopes_required(func):
    def wrapper(*args, **kwargs):
        shop = kwargs.get("shop")

        try:
            configured_access_scopes = apps.get_app_config(
                "shopify_app").SHOPIFY_API_SCOPES
            current_access_scopes = shop.access_scopes

            assert ApiAccess(configured_access_scopes) == ApiAccess(
                current_access_scopes)
        except:
            kwargs["scope_changes_required"] = True

        return func(*args, **kwargs)

    return wrapper
