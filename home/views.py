from django.shortcuts import render

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

def search_view(request, *args, **kwargs):
    response = render(request, 'search.html', {})
    response.delete_cookie('fe_used')
    response.delete_cookie('comp')
    response.delete_cookie('element_set')
    response.delete_cookie('num_element')
    response.delete_cookie('num_atom')
    response.delete_cookie('prototype')
    response.delete_cookie('spacegroup')
    response.delete_cookie('fe_enable_or_not')
    response.delete_cookie('formation_energy')


    return response

def forum_view(request, *args, **kwargs):
    return render(request, 'forum.html', {})

def contact_view(request, *args, **kwargs):
    return render(request, 'contact.html', {})

