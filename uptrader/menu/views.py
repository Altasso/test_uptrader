from django.shortcuts import render, get_object_or_404
from .models import MenuItem

# Create your views here.
def home(request):
    return render(request, 'base.html')

def dynamic_page(request, slug):
    path = '/' + slug.strip('/') + '/'
    menu_item = get_object_or_404(MenuItem, url=path)
    return render(request, 'dynamic_page.html', {'menu_item': menu_item})