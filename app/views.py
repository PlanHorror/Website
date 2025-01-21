from django.shortcuts import render

# Create your views here.
def index(request):
    # Print template root directory
    # print('Template root directory:', request.templates.dirs)
    return render(request, 'member/index.html')