# Create your views here.
import math
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from sweetrs.recommender.forms import ProductForm
from sweetrs.recommender.models import Product
from recommender.models import Rating
from django.views.decorators.csrf import csrf_exempt                                          

PRODUCTS_ON_SITE = 1

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def facebook_intro(request):
    return render_to_response('intro.html',
        context_instance=RequestContext(request, {
        }
    ))

@csrf_exempt
def product_reviews(request, template_path='products.html'):
    """ list products """

    products = Product.objects.all()
    if request.user.is_authenticated():
        products = products.exclude(id__in = Rating.objects.filter(user=request.user).values_list('product__id', flat=True))

    all = Product.objects.all().count()
    if request.user.is_authenticated():
        rated = Rating.objects.filter(user=request.user).count()
    else:
        rated = 0
    ratingbar = 0
    if all > 0:
        ratingbar = rated * 500 / all

    return render_to_response(template_path,
        context_instance=RequestContext(request, {
            "products": products.order_by("?")[:PRODUCTS_ON_SITE],
            "all": all,
            "rated": rated,
            "ratingbar": ratingbar
        }
    ))

def get_ratings_vector(user):
    ratings = Rating.objects.filter(user=user, value__gt = 0).values('product_id','value')
    res = {}
    for r in ratings:
        res[r['product_id']] = r['value']
    return res

def vector_corelation_tau(v1,v2):
    tau = 0
    n = 0

    for k in v1.keys():
        val1 = v1[k] - 3
        val2 = v2.get(k,None)
        if val2 == None:
            continue
        val2 = val2 - 3
        n = n+1
        if val1 * val2 > 0:
            tau += 1
        if val1 * val2 < 0:
            tau -= 1
    if n==0:
        return None

    return float(tau) / float(n)

def vector_corelation_pearson(v1,v2):
    tau = 0
    n = 0
    stdev1 = 0
    stdev2 = 0

    for k in v1.keys():
        val1 = v1[k] - 3
        val2 = v2.get(k,None)
        if val2 == None:
            continue
        val2 = val2 - 3
        n = n+1
        tau += val1 * val2

        stdev1 += val1 * val1
        stdev2 += val2 * val2
    if n==0:
        return None

    return float(tau) / (math.sqrt(stdev1/float(n)) * math.sqrt(stdev2/float(n)) * float(n))

def predict_rating(product, vector_corr):
    ratings = Rating.objects.filter(product=product, value__gt = 0).values('user_id','value')
    res = 0
    normalizer = 0

    for r in ratings:
        coeff = vector_corr.get(r['user_id'], None)
        if not coeff or coeff < 0:
            continue
        res += coeff * r['value']
        normalizer += coeff

    if normalizer:
        return res / normalizer

    return None

def product_recommends(request, template_path='recommends.html'):
    products = Product.objects.all()

    if request.user.is_anonymous():
        return render_to_response('recommends.html',
            context_instance=RequestContext(request, {}))

    # find similar users:
    users = User.objects.all().exclude(id=request.user.id).select_related('facebookprofile')
    v1 = get_ratings_vector(request.user)


    vector_corr = {}
    users_with_corr = []
    for u in users:
        v2 = get_ratings_vector(u)
        tau = vector_corelation_pearson(v1,v2)
        if tau == None:
            continue
        vector_corr[u.id] = tau
        u.tau = tau

        users_with_corr.append(u)

    users_with_corr.sort(lambda x, y: cmp(x.tau,y.tau),None,True)

    products_with_marks = []
    for p in products:
        rating = 0
        try:
            rating_obj = Rating.objects.get(user=request.user, product=p)
            rating = rating_obj.value
        except:
            pass

        predict = predict_rating(p, vector_corr)
        if not predict:
            continue

        p.difference = 0

        if rating > 0:
            p.difference = abs(rating - predict)

        if rating == 0:
            rating = 'n/a'

        p.rating = rating
        p.predict = predict

        products_with_marks.append(p)

    products_with_marks.sort(lambda x, y: cmp(x.predict,y.predict),None,True)

    return render_to_response(template_path,
        context_instance=RequestContext(request, {"products_with_marks": products_with_marks,
                                                  "users_with_corr": users_with_corr}))

def product_add(request):
    """ list products """
    if request.POST and request.FILES:
        # dane z POST
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_reviews')
    else:
        # formularz
        form = ProductForm()

    return render_to_response('product.add.html',
        context_instance=RequestContext(request, {"form": form}))

@csrf_exempt
def product_rate(request):
    """ list products """
    if request.user.id == None:
        username = random.randint(10000000, 99999999).__str__()
        email = random.randint(10000000, 99999999).__str__() + "@dummy.sweetrs.org"
        password = random.randint(10000000, 99999999).__str__()
        user = User.objects.create_user(username, email, password)
        request.user = authenticate(username=username,password=password)
        login(request, request.user)
    id = request.POST['id']

    product = Product.objects.get(id=id)
    rating, created = Rating.objects.get_or_create(product = product, user = request.user)
    rating.value = request.POST['val']
    rating.save()
    try:
        products = Product.objects.all().exclude(id__in = Rating.objects.filter(user=request.user).values_list('product__id', flat=True))
        product = products.order_by("?")[0]
    except:
        return HttpResponse("You have already rated all sweets. Thanks! Now you can check recommends!")

    return render_to_response('include/product.html',
        context_instance=RequestContext(request, {"item": product}))

