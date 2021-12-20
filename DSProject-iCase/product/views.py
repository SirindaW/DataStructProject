from django.shortcuts import render,get_object_or_404
from .models import CollectionFeature, IphoneModel, Product
from django.http import Http404,QueryDict
from django.core.exceptions import ObjectDoesNotExist
from DS.sorting import sort_by_price, sort_by_alphabet
from django.http import JsonResponse
from DS.ProductStructure import ProductStructure


# Create your views here.

def product_view(request):
    # QueryDict get list for the specified key.
    models = QueryDict.getlist(request.GET,'model')
    print("MODEL:",models)
    # for k in request.GET:
    #     print(request.GET.get('model'))
    #     print(k,request.GET[k])
    collections = QueryDict.getlist(request.GET,'collection')
    print("COLLECTION:",collections)

    prices = QueryDict.getlist(request.GET,'price')
    print("PRICE:",prices)

    # Title
    legend = 'iPhone เคส'

    # Fetch data base
    products_db = Product.objects.all()
    # Convert to product structures
    product_s = ProductStructure(products_db)

    # Model Filter
    # if request.GET.get('model'):
    #     selected = []
    #     for k in allproducts:
    #         if k.model.is_model(request.GET.get('model')):
    #             selected.append(k)
    #     allproducts = selected

    #     # legend title
    #     allmodels = IphoneModel.objects.all()
    #     for m in allmodels:
    #         if m.is_model(request.GET.get('model')):
    #             legend = m.title

    # Model Filter (New)
    if request.GET.get('model'):
        selected = ProductStructure()
        for k in product_s:
            if k.product.model.is_model(request.GET.get('model')):
                selected.add(k.product)
        product_s = selected

        # legend title
        allmodels = IphoneModel.objects.all()
        for m in allmodels:
            if m.is_model(request.GET.get('model')):
                legend = m.title


    # Collection Filter
    # if request.GET.get('collection'):
    #     selected = []
    #     list_of_collections = QueryDict.getlist(request.GET,'collection')
    #     # check if k in list_of_collections
    #     for k in allproducts:
    #         for c in list_of_collections:
    #             if k.collection.is_collection(c):
    #                 selected.append(k)
    #                 break
    #     allproducts=selected
            

    # Collection Filter (NEW)
    if request.GET.get('collection'):
        selected = ProductStructure()
        list_of_collections = QueryDict.getlist(request.GET,'collection')
        # check if k in list_of_collections
        for k in product_s:
            for c in list_of_collections:
                if (k.product.collection):
                    # if has collection
                    if k.product.collection.is_collection(c):
                        selected.add(k.product)
                        break
        product_s = selected
        

    # Order options
    mode = {}
    if request.GET.get('order'):
        # sort by price
        if request.GET.get('order') == "price-asc":
            mode = dict.fromkeys(['price'],True)
            rev = False
            asc = True
        elif request.GET.get('order') == "price-desc":
            mode = dict.fromkeys(['price'],True)
            rev = True
            asc = False

        # sort by alphabet 
        if request.GET.get('order') == "alpha-asc":
            mode = dict.fromkeys(['alpha'],True)
            mode.fromkeys(['alpha'])
            rev= False
            asc=True
        elif request.GET.get('order') == "alpha-desc":
            mode = dict.fromkeys(['alpha'],True)
            mode.fromkeys(['alpha'])
            rev = True
            asc=False

    if mode.get('price'):
        product_s = product_s.sort_by_price(asc)
        # allproducts = [p.product for p in product_s.sort_by_price(asc)]
        # allproducts = sort_by_price(allproducts,rev)
    elif mode.get('alpha'):
        product_s = product_s.sort_by_alphabet(asc)
        # allproducts = [p.product for p in product_s.sort_by_alphabet(asc)]
        # allproducts = sort_by_alphabet(allproducts,rev)

    # Search case
    # HASH SEARCHING
    if request.GET.get('search'):
        key = request.GET.get('search')
        ex_match = product_s.get_or_none(name=key)
        if ex_match is not None:
            product_id = ex_match.product.id

            # BINARY SEARCH TREE (SEARCHING by id)
            item = product_s.binary_search_id(product_id)
            if item is not None:
                product_s = [item]
            else:
                product_s = []
        else:
            # Not match any
            product_s = []

    allproducts = [p.product for p in product_s]

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
