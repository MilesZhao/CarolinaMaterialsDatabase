import re,collections
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
from django.http import HttpResponse


# Create your views here.

def demo_view(request):

    demo_id = int(request.GET["demo_id"])
    if demo_id == 1:
        query_id = [11500, 924, 13074, 4758, 340, 13148, 7215, 262, 12123, 12932, 9888, 419, 12084, 6633, 6314, 7156, 2343, 12692, 8198, 8056, 1324, 1927, 9762, 3432, 11988]
        typ = 'ABC<sub>6</sub>-216'
    elif demo_id == 2:
        query_id = [13873, 13925, 14166, 14234, 13952, 14095, 14230, 14130, 13951, 14135, 14041, 14231, 14322, 14189, 14214, 14256, 14025, 14263, 13980, 14405, 14365, 13998, 14070, 14136, 14182]
        typ = 'AB<sub>6</sub>C<sub>6</sub>-225'
    elif demo_id == 3:
        query_id = [17856, 17045, 26518, 22313, 22386, 26493, 20506, 18730, 15019, 26413, 20822, 17440, 18545, 23107, 22982, 24199, 25141, 18682, 29156, 28959, 30243, 23350, 25091, 25534, 26961]
        typ = 'ABCD<sub>6</sub>-216'
    elif demo_id == 4:
        query_id = [36357, 36736, 34948, 34963, 33271, 32001, 31677, 34051, 34234, 34707, 32244, 35940, 33827, 34148, 35110, 36412, 33940, 34789, 34495, 36567, 34164, 31793, 31585, 31767, 36707]
        typ = 'ABC<sub>6</sub>D<sub>6</sub>-216'
    else:
        query_id = []

    mat = Entry.objects.filter(id__in = query_id)
    if mat != None:
        results = mat.order_by('id')
        
        response = render(request, 'show_demo.html', {'results': results, 'type':typ})
    else:
        response = render(request, 'show_demo.html', {})

    return response

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
    valid_keys = {'comp', 'element_set',\
                  'num_element', 'num_atom', 'prototype',\
                  'spacegroup', 'fe_used', 'formation_energy'}
    for k in cookie:
        if k not in valid_keys:
            continue
        if k == 'csrftoken':
            continue
        if k == 'formation_energy':
            d[k] = cookie[k]
            continue
        if k == 'element_set':
            d[k] = cookie[k]
            continue
        if k == 'comp':
            d[k] = cookie[k]
            continue

        d[k] = eval(cookie[k])
    return d

def sub_formula(d):
    s = ''
    for k in d:
        if int(d[k]) == 1:
            s += str(k)
            continue
        s += str(k) +'<sub>'+str(int(d[k]))+'</sub>'
    return s

def _parse_formula(formula):
    formula = formula.replace("@", "")

    def get_sym_dict(f, factor):
        sym_dict = collections.defaultdict(float)
        for m in re.finditer(r"([A-Z][a-z]*)\s*([-*\.\d]*)", f):
            el = m.group(1)
            amt = 1
            if m.group(2).strip() != "":
                amt = float(m.group(2))
            sym_dict[el] += amt * factor
            f = f.replace(m.group(), "", 1)
        if f.strip():
            return 
        return sym_dict

    m = re.search(r"\(([^\(\)]+)\)\s*([\.\d]*)", formula)
    if m:
        factor = 1
        if m.group(2) != "":
            factor = float(m.group(2))
        unit_sym_dict = get_sym_dict(m.group(1), factor)
        expanded_sym = "".join(["{}{}".format(el, amt)
                                for el, amt in unit_sym_dict.items()])
        expanded_formula = formula.replace(m.group(), expanded_sym)
        return _parse_formula(expanded_formula)
    return get_sym_dict(formula, 1)

def is_str_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def mat_detail_view(request):

    is_cookie_ready = False

    cookie_keys = set(request.COOKIES.keys())
    post_keys = set(request.POST.dict().keys())
    # print(request.POST)
    # print()
    # print((cookie_keys & post_keys))
    #print('cookie keys: ', cookie_keys)
    valid_keys = {'comp', 'element_set',\
                  'num_element', 'num_atom', 'prototype',\
                  'spacegroup', 'fe_used', 'formation_energy'}
    if len(set(cookie_keys)&valid_keys) >= 1:
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
        c = _parse_formula(request_set['comp'])
        if c:
            mat = Entry.objects.filter(formula = sub_formula(c))
        else:
            return render(request, 'invalid.html', {'invalid_query': request_set['comp'], 'field': 'Composition'})

    if 'element_set' in request_set and request_set['element_set']:
        s = request_set['element_set']
        ls = '-'.join(sorted(s.split('-')))
        if mat == None:
            mat = Entry.objects.filter(element_list = ls)
        else:
            mat = mat.filter(element_list = ls)

    if 'num_element' in request_set and request_set['num_element']:
        if not is_str_int(request_set['num_element']):
            return render(request, 'invalid.html', {'invalid_query': request_set['num_element'], 'field': '# of Elements'})

        if mat == None:
            mat = Entry.objects.filter(nelement = request_set['num_element'])
        else:
            mat = mat.filter(nelement = request_set['num_element'])

    if 'num_atom' in request_set and request_set['num_atom']:
        if not is_str_int(request_set['num_atom']):
            return render(request, 'invalid.html', {'invalid_query': request_set['num_atom'], 'field': '# of Atoms'})

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
        mat = mat.order_by('id')
    
        page = request.GET.get('page', 1)

        paginator = Paginator(mat, 10)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        
        response = render(request, 'show_page.html', {'results': results,'tot_results':"{:,d}".format(mat.count())})
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
    
