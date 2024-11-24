from django.http import HttpResponse
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def hello(request):
    return HttpResponse('Hello World!')