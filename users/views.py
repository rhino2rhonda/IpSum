from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import RequestContext, loader
from datetime import datetime
from django.contrib.auth import logout
from shops.models import Shop, Catalog, ShopUserRelation
from users.models import UserProfile
from products.models import Product

@login_required
def HomeView(request,shopid=None):
    home=True
    if request.user.groups.filter(name='consumers'):
        visits = int(request.COOKIES.get('visits', '0'))
        if request.session.get('last_visit'):
            last_visit_time = request.session.get('last_visit')
            visits = request.session.get('visits', 0)
            if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 7:
                request.session['visits'] = visits + 1
                request.session['last_visit'] = str(datetime.now())
        else:
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = 1
        if request.session.get('visits'):
                count = request.session.get('visits')
        else:
            count = 0
        return render_to_response("user/home.html", {'visits':count,'home':home}, context_instance=RequestContext(request))
    

    elif request.user.groups.filter(name='shopadmin'):
        context = {}
        shops = request.user.shop_set.all()
        context['shops'] = shops
        #check if shop if specified
        if shopid == None:
            shops = request.user.shop_set.all()
            if shops:
                shop = shops[0]
            else:
                shop = None
        #test that perms for specified shop exists
        else:
            try:
                shop = Shop.objects.get(id = shopid)
                if not shop.shop_admin.id == request.user.id:
                    raise Exception
            except:
                return HttpResponse("The requested shop does not exist or is inaccessible for this current shopadmin.")

        context["shop"] = shop
        print str(shop)
        return render_to_response("shops/shop_home.html", context, context_instance=RequestContext(request))


    elif request.user.groups.filter(name='admin'):
        return HttpResponse("admin_home")


    else:
        return HttpResponse("invalid group")


@login_required
def FindShopsView(request):
    template_name = 'user/findShops.html'
    context_object_names = ['shop_list', 'queryString']
    if request.method == 'POST':
        queryString = request.POST['querystring']
        shopList = Shop.objects.filter(shop_name__contains=queryString)
        context_objects = [shopList, queryString]
    else:
        queryString = ''
        shopList = Shop.objects.all()
        context_objects = [shopList, queryString]
    context = dict(zip(context_object_names, context_objects))
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
def ShopView(request, shopid):
    template_name = 'user/shop_view.html'
    context_objects_name = ('shop',
                            'shop_catalog',
                            'shop_visited',
                            'shop_liked',
                            'like_button',
                            'visited_button',
                            'loyalty_points')
    print "8888888888888"    
    user = request.user
    shop = Shop.objects.get(id=shopid)
    like_button=False
    visited_button = False


    relation,created = ShopUserRelation.objects.get_or_create(shop=shop,user=user)

    if request.POST.get('like_button'):
        like_button=True
        relation.user_like = True
        relation.loyalty_points += 50
    if request.POST.get('visited_button'):
        visited_button = True
        relation.user_like = True
        relation.loyalty_points += 100
    
    loyalty_points = relation.loyalty_points

    context_objects = (shop, shop.catalog_set.all(),relation.visited,relation.user_like,loyalty_points)
    context = RequestContext(request, dict(zip(context_objects_name,context_objects)))
    
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context))


@login_required
def FindProductsView(request):
    template_name = 'user/findProducts.html'
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

@login_required
def AllSellersView(request, prodid):
    template_name = 'user/allSellers.html'
    context_objects_name = ('catalogItems', 'product')
    p = Product.objects.get(id=prodid)
    catalogItems = p.catalog_set.all()
    context_objects = (catalogItems, p)
    context = RequestContext(request, dict(zip(context_objects_name,context_objects)))
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context))



@login_required
def OfferView(request):
    context= RequestContext(request)
    context = {"SiteOffers" : None}

    #shopOffers
    shops = Shop.objects.all()
    ShopOffers = []
    for s in shops:
        offers = s.shopoffer_set.all()
        if offers:
            ShopOffers.append((offers))
    context["ShopOffers"] = ShopOffers

    #productOffers
    ProductOffers = []
    catalog_items = Catalog.objects.all()
    for c in catalog_items:
        offers = c.productoffer_set.all()
        if offers:
            ProductOffers.append((offers))
    context["ProductOffers"] = ProductOffers
    print (ShopOffers)
    print ProductOffers

    return render_to_response("user/offers.html",context,context_instance=RequestContext(request))


@login_required
def PointsView(request):
    user=request.user
    relations = request.user.shopuserrelation_set.all()
    context = {}
    context['relations'] = relations
    agg = request.user.shopuserrelation_set.aggregate(Sum("loyalty_points"))
    points = agg['loyalty_points__sum']
    if not points:
        points = 0
    context["loyalty_points"] = points
    print points
    return render_to_response("user/points.html",context,context_instance=RequestContext(request))