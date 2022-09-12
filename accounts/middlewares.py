from .models import IpAddress


class SaveIpAddress:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        obj, created = IpAddress.objects.get_or_create(ip=ip)

        request.user.ip_address = obj

        response = self.get_response(request)
        return response


class CheckSubscription:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.is_special_user()

        response = self.get_response(request)
        return response
