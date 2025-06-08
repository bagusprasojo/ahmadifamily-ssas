# treeapp/middleware.py
from .models import VisitorLog

class VisitorLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Hindari mencatat request ke admin atau static/media
        if not request.path.startswith('/admin') and not request.path.startswith('/static'):
            ip = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            referer = request.META.get('HTTP_REFERER', '')
            VisitorLog.objects.create(
                path=request.path,
                ip_address=ip,
                user_agent=user_agent,
                referer=referer
            )

        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
