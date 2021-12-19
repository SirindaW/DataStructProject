from django.shortcuts import render,get_object_or_404
from .models import CollectionFeature, IphoneModel, Product
from django.http import Http404,QueryDict
from django.core.exceptions import ObjectDoesNotExist
from DS.sorting import sort_by_price, sort_by_alphabet
from django.http import JsonResponse


# Create your views here.

def product_view(request):
    # QueryDict get list for the specified key.
    models = QueryDict.getlist(request.GET,'model')
    print("MODEL:",models)
    # for k in request.GET:
    #     print(request.GET.get('model'))
        # print(k,request.GET[k])
    collections = QueryDict.getlist(request.GET,'collection')
    print("COLLECTION:",collections)

    # Title
    legend = 'iPhone เคส'

    # Fetch data base
    allproducts = Product.objects.all()

    # Model Filter
    if request.GET.get('model'):
        selected = []
        for k in allproducts:
            if k.model.is_model(request.GET.get('model')):
                selected.append(k)
        allproducts = selected

        # legend title
        allmodels = IphoneModel.objects.all()
        for m in allmodels:
            if m.is_model(request.GET.get('model')):
                legend = m.title

    # Collection Filter
    if request.GET.get('collection'):
        selected = []
        list_of_collections = QueryDict.getlist(request.GET,'collection')
        # check if k in list_of_collections
        for k in allproducts:
            for c in list_of_collections:
                if k.collection.is_collection(c):
                    selected.append(k)
                    break
        allproducts=selected
            
        

    # Order options
    mode = {}
    if request.GET.get('order'):

        # sort by price
        if request.GET.get('order') == "price-asc":
            mode = dict.fromkeys(['price'],True)
            rev = False
        elif request.GET.get('order') == "price-desc":
            mode = dict.fromkeys(['price'],True)
            rev = True

        # sort by alphabet 
        if request.GET.get('order') == "alpha-asc":
            mode = dict.fromkeys(['alpha'],True)
            mode.fromkeys(['alpha'])
            rev= False
        elif request.GET.get('order') == "alpha-desc":
            mode = dict.fromkeys(['alpha'],True)
            mode.fromkeys(['alpha'])
            rev = True

    if mode.get('price'):
        allproducts = sort_by_price(allproducts,rev)
    elif mode.get('alpha'):
        allproducts = sort_by_alphabet(allproducts,rev)


    context = {
        'legend_title': legend,
        'allproducts': allproducts
    }

    return render(request, 'cases.html', context)


def product_collections_view(request):


    # Collection Filter
    if request.GET.get('collection-filter'):
        print('filtering')
        print(request.GET.get('collection-filter'))
        allproducts= []
        all_collection_products= [obj for obj in Product.objects.all()
                    if obj.collection is not None]
        for k in all_collection_products:
            if k.collection.is_collection(request.GET.get('collection-filter')):
                print(k.title)
                print(k.collection)
                allproducts.append(k)

        # legend title
        all_collections = CollectionFeature.objects.all()
        for m in all_collections:
            if m.is_collection(request.GET.get('collection-filter')):
                legend = m.title
    else:
        legend = "คอลเลคชั่น"
        allproducts = [obj for obj in Product.objects.all()
                    if obj.collection is not None]


    # Order options
    mode = {}
    if request.GET.get('order'):

        # sort by price
        if request.GET.get('order') == "price-asc":
            mode = dict.fromkeys(['price'],True)
            rev = False
        elif request.GET.get('order') == "price-desc":
            mode = dict.fromkeys(['price'],True)
            rev = True

        # sort by alphabet 
        if request.GET.get('order') == "alpha-asc":
            mode = dict.fromkeys(['alpha'],True)
            mode.fromkeys(['alpha'])
            rev= False
        elif request.GET.get('order') == "alpha-desc":
            mode = dict.fromkeys(['alpha'],True)
            mode.fromkeys(['alpha'])
            rev = True

    if mode.get('price'):
        allproducts = sort_by_price(allproducts,rev)
    elif mode.get('alpha'):
        allproducts = sort_by_alphabet(allproducts,rev)


    context = {
        'legend_title': legend,
        'allproducts': allproducts
    }

    return render(request, 'collection.html', context)


def product_test_filter(request):
    return render(request, 'product/test_product_filter.html')


def product_detail_view(request, product_slug):
    # obj = Product.objects.get(slug=product_slug)
    obj = get_object_or_404(Product,slug=product_slug)

    context = {'obj': obj}

    return render(request, 'product/detail.html', context)
