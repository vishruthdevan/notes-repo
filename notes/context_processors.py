from django.conf import settings
from .models import *

def leader_board(request):
    leaders = Author.objects.all().order_by('-exp')[:10]
    return {'leaders' : leaders}
