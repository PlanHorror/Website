from django.shortcuts import render
from members.models import *
from django.utils.translation import gettext as _, get_language, activate
# Create your views here.
def index(request):
    # Print template root directory
    # print('Template root directory:', request.templates.dirs)
    return render(request, 'app/tem/index.html')