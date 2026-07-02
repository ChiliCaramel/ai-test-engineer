from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from pracdjango import models
from pracdjango.decorator import rate_limit

# Create your views here.
@rate_limit(requests_per_day=4)
@require_http_methods(["POST"])
def requests_ip_addr(request):

    return JsonResponse({'msg':'ok'},status = 200)
