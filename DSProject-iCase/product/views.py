from django.shortcuts import render
from .models import Product
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from DS.sorting import sort_by_price, sort_by_alphabet


# Create your views here.

def filter_below_price(data, price):
    result = []
    for d in data:
        # Check compare value here.
        value = d.price
        if value <= price:
            result.append(d)

    return result


def product_view(request):

    allproducts = Product.objects.all()

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
    obj = Product.objects.get(slug=product_slug)

    context = {'obj': obj}

    return render(request, 'product/detail.html', context)
