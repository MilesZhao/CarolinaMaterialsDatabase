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
        query_id = [37356,37841,37938,\
        13148, 12932, 419, 7378, 14130, 14322, 14365, 14136, 13863,\
        14255, 12123, 8068, 262, 4668, 9888, 13980, 10469, 4395, 9631,\
        4515, 10153, 4853, 14189, 12128, 14405, 13998, 6944, 7245, 14256,\
        14263, 4307, 4884, 6866, 13383, 13040, 14041, 2627, 3966, 3432,\
        7811, 710, 13691, 1914, 182, 2999, 8243, 2035, 2042, 10521, 1027, 924, 7854, 14230, 4303, 8138, 11934, 1937, 4235, 13027, 3342, 2144, 10277, 13951, 8400, 10490, 14182, 5405, 558, 13206, 11501, 5803, 8954, 3322, 13055, 11851, 2038, 11246, 11693, 11988, 9762, 8056, 3454, 12876, 4521, 4227, 11771, 1650, 2099, 12214, 7430, 11892, 4594, 11282, 13106, 14025, 11840, 10832, 14413, 14306, 11500, 14330, 1195, 9769, 7602, 6308, 10046, 12502, 4421, 6633, 5834, 12084, 4887, 14072, 2791, 410, 4275, 12717, 6161, 2081, 6912, 12902, 1542, 2343, 8198, 4758, 7471, 10107, 12152, 13952, 12692, 4871, 8666, 7215, 10057, 445, 14231, 8385, 1459, 9142, 14095, 6945, 7156, 10351, 13119, 14070, 9354, 14374, 14135, 1100, 1927, 13794, 14047, 9672, 6314, 9058, 14234, 13955, 6734, 13074, 3283, 4637, 14329, 6848, 7598, 14088, 13005, 1187, 14375, 340, 8319, 1324, 14214, 14299, 6436, 8070, 10630, 14257, 14066, 14268, 13898, 13873, 13925, 14166]
        typ = 'ternary'
        num = '186'
    elif demo_id == 2:
        query_id = [22313, 25498, 18625, 28343, 17604, 31546, 26007, 26210, 21570, 18545, 24174, 17178, 19275, 15791, 19462, 16498, 31133, 18629, 24598, 19867, 22457, 18509, 14465, 30137, 26963, 19000, 29398, 30974, 30809, 21283, 24101, 25141, 29824, 17264, 23755, 28574, 26104, 25893, 30896, 29592, 14912, 17783, 29491, 20369, 20487, 20714, 23644, 21521, 15669, 21917, 31293, 20647, 30121, 27021, 27769, 30534, 29089, 23462, 15609, 22838, 15493, 23509, 22278, 19728, 28543, 17045, 25573, 21769, 31044, 29869, 28800, 14785, 16943, 28327, 23022, 30341, 16576, 19783, 24619, 29104, 20903, 30849, 16024, 21850, 20506, 26961, 23436, 27144, 23842, 26413, 15019, 19059, 31200, 27673, 27563, 15207, 17350, 27150, 24116, 18017, 26493, 30168, 20618, 28601, 22386, 25437, 30699, 20475, 25080, 14619, 18924, 23252, 24912, 25591, 24505, 31053, 18418, 14991, 14687, 31424, 21750, 28959, 18791, 21925, 17680, 29951, 29926, 19084, 31231, 17764, 26561, 24746, 15934, 24630, 26831, 29149, 19745, 23946, 34247, 29462, 17363, 19468, 30378, 17464, 19963, 14447, 16447, 35350, 31245, 20822, 27438, 18934, 23107, 27645, 19315, 15037, 25873, 26518, 28455, 21392, 25997, 22505, 14595, 22252, 18603, 20691, 19951, 25299, 17552, 20300, 28848, 25313, 23350, 18899, 32244, 17873, 36567, 16522, 14564, 34495, 30319, 23042, 22533, 26296, 28980, 16443, 22566, 20285, 25534, 24199, 19750, 19782, 35940, 28804, 33827, 23286, 15305, 25315, 27933, 31380, 19544, 35895, 28043, 19741, 27752, 17053, 30243, 15981, 17364, 16202, 22928, 32822, 36679, 26442, 24928, 18682, 25748, 34234, 25206, 17639, 16019, 31015, 31523, 33700, 19025, 16600, 18154, 19794, 36736, 27245, 27285, 30093, 33008, 22924, 18927, 35083, 14817, 28615, 27845, 27223, 20113, 17440, 35167, 28109, 26262, 35701, 36707, 14562, 23019, 34035, 32530, 33202, 31677, 31767, 34948, 34148, 30943, 33480, 34601, 34319, 32472, 25734, 27173, 30543, 23275, 17462, 32001, 29156, 34164, 22982, 31793, 18730, 34963, 35110, 35021, 25091, 19142, 34051, 34216, 34237, 35545, 35746, 31585, 14841, 33271, 25278, 17856, 26662, 26584, 25738, 15369, 35981, 33940, 34707, 33754, 34789, 34254, 28578, 26641, 36479, 36412, 36357, 25207, 36844, 17752, 24774, 18590, 28666, 27159, 27975, 26697, 29385, 22401, 31869, 34381, 34834, 36334, 33183, 36819, 35014, 35359, 33421, 35851]
        typ = 'quaternary'
        num = '323'
    else:
        query_id = []

    mat = Entry.objects.filter(id__in = query_id)
    if mat != None:
        results = mat.order_by('id')
        
        response = render(request, 'show_demo.html', {'results': results, 'type':typ, 'number':num})
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
    
