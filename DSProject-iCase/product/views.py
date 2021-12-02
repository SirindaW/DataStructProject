from django.shortcuts import render,get_object_or_404
from .models import Product
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from DS.sorting import sort_by_price, sort_by_alphabet


# Create your views here.

def product_view(request):

    # for k in request.GET:
    #     print(k,request.GET[k])

    # Model Filter
    if request.GET.get('model'):
        allproducts = []
        for k in Product.objects.all():
            if k.model.is_model(request.GET.get('model')):
                allproducts.append(k)
    else:
        allproducts = Product.objects.all()


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
        'allproducts': allproducts
    }

    return render(request, 'cases.html', context)


def product_collections_view(request):

    allproducts = [obj for obj in Product.objects.all()
                   if obj.collection is not None]

    if request.GET.get('price-order'):
        if request.GET.get('price-order') == "asc":
            rev = False
        elif request.GET.get('price-order') == "desc":
            rev = True

        allproducts = sort_by_price(allproducts, rev)

    if request.GET.get('alpha-order'):
        if request.GET.get('alpha-order') == "asc":
            rev = False
        elif request.GET.get('alpha-order') == "desc":
            rev = True

        allproducts = sort_by_alphabet(allproducts, rev)

    context = {'allproducts': allproducts}
    return render(request, 'collection.html', context)


def product_test_filter(request):
    return render(request, 'product/test_product_filter.html')


def product_detail_view(request, product_slug):
    # obj = Product.objects.get(slug=product_slug)
    obj = get_object_or_404(Product,slug=product_slug)

    context = {'obj': obj}

    return render(request, 'product/detail.html', context)
