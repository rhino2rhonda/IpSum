from django.template import RequestContext, loader
from django.http import HttpResponse
from products.models import Product
from shops.models import Shop, Catalog
from django.shortcuts import render_to_response

# Create your views here.

def FindProductsView(request):
    template_name = 'products/findProducts.html'
    context_object_names = ['product_list', 'queryString']
    if request.method == 'POST':
        queryString = request.POST['querystring']
        productList = Product.objects.filter(product_name__contains=queryString)
        context_objects = [productList, queryString]
    else:
        queryString = ''
        productList = Product.objects.all()
        context_objects = [productList, queryString]
    context = dict(zip(context_object_names, context_objects))
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def AllSellersView(request, prodid):
    template_name = 'products/allSellers.html'
    context_objects_name = ('catalogItems', 'product')
    p = Product.objects.get(id=prodid)
    catalogItems = p.catalog_set.all()
    context_objects = (catalogItems, p)
    context = RequestContext(request, dict(zip(context_objects_name,context_objects)))
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context))
