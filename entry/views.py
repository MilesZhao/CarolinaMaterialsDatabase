from django.shortcuts import render,get_object_or_404
from .models import Entry, Spacegroup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView
)


# Create your views here.

class EntryDetailView(DetailView):
    template_name = 'entry/detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Entry, id=id_)

        

def post2dict(post):
    keys = post.dict().keys()
    d = {}
    for k in keys:
        if k in ['prototype','spacegroup']:
            d[k] = post.getlist(k)
        else:
            d[k] = post[k]
    return d

def eval_cookie(cookie):
    d = {}
    for k in cookie:
        if k == 'csrftoken':
            continue
        if k == 'formation_energy':
            d[k] = cookie[k]
            continue
        d[k] = eval(cookie[k])
    return d

def mat_detail_view(request):

    is_cookie_ready = False

    cookie_keys = set(request.COOKIES.keys())
    post_keys = set(request.POST.dict().keys())
    # print(request.POST)
    # print()
    # print((cookie_keys & post_keys))
    #print('cookie keys: ', cookie_keys)
    if len(cookie_keys) > 1:
        request_set = eval_cookie(request.COOKIES)
        is_cookie_ready = True
        #print('Cookie is here')
    else:
        request_set = post2dict(request.POST)
        if request.POST.getlist('fe_enable_or_not'):
            request_set['fe_used'] = True
        else:
            request_set['fe_used'] = False

    # print(request.COOKIES.keys())
    # print(type(request.COOKIES))
    # print(request_set)
    #print('query keys: ', request_set)

    mat = None
    if 'comp' in request_set and request_set['comp']:
        mat = Entry.objects.filter(formula = request_set['comp'])

    if 'element_set' in request_set and request_set['element_set']:
        s = request_set['element_set']
        ls = '-'.join(sorted(s.split('-')))
        if mat == None:
            mat = Entry.objects.filter(element_list = ls)
        else:
            mat = mat.filter(element_list = ls)

    if 'num_element' in request_set and request_set['num_element']:
        if mat == None:
            mat = Entry.objects.filter(nelement = request_set['num_element'])
        else:
            mat = mat.filter(nelement = request_set['num_element'])

    if 'num_atom' in request_set and request_set['num_atom']:
        if mat == None:
            mat = Entry.objects.filter(natom = request_set['num_atom'])
        else:
            mat = mat.filter(natom = request_set['num_atom'])

    if 'prototype' in request_set and request_set['prototype']:
        # print('in prototype', request_set['prototype'])
        if mat == None:
            mat = Entry.objects.filter(generic__in = request_set['prototype'])
        else:
            mat = mat.filter(generic__in = request_set['prototype'])
 
    if 'spacegroup' in request_set and request_set['spacegroup']:
        if mat == None:
            mat = Entry.objects.filter(spacegroup__in = request_set['spacegroup'])
        else:
            mat = mat.filter(spacegroup__in = request_set['spacegroup'])

    if 'fe_used' in request_set and request_set['fe_used'] and 'formation_energy' in request_set and request_set['formation_energy']:
        low,high = eval(request_set['formation_energy'])
        if mat == None:
            mat = Entry.objects.filter(formation_energy__gte=low).\
                filter(formation_energy__lte=high)
        else:
            mat = mat.filter(formation_energy__gte=low).\
                filter(formation_energy__lte=high)
    
    if mat != None:
        print(mat.count())
    else:
        print(0)

    if mat != None:
        mat = mat.order_by('id')
    
        page = request.GET.get('page', 1)

        paginator = Paginator(mat, 10)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        
        response = render(request, 'show_page.html', {'results': results,'tot_results':mat.count()})
    else:
        response = render(request, 'show_page.html', {'tot_results':0})
    
    if is_cookie_ready == False:
        for k in post_keys:
            if k == 'fe_enable_or_not' or k == 'csrfmiddlewaretoken':
                continue
            if request_set[k]:
                if k == 'formation_energy' and not request_set['fe_used']:
                    continue
                # print(k, type(request_set[k]))
                response.set_cookie(k, request_set[k])
        if request_set['fe_used']:
            response.set_cookie('fe_used', True)
    return response
    
