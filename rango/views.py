# ---------------------------------------------------******  Imports  ******--------------------------------------------
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm

import json

# ---------------------------------------------------****** Creating views ******---------------------------------------


# ---------------------------------------------------******  Main Home Page  ******-------------------------------------
def rango_index(request):
    '''
    Testing cookie
    request.session.set_test_cookie()
    '''
    # top 5 catagories
    category_list = Category.objects.order_by('-likes')[:5]
    # top 5 pages
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories' : category_list}
    context_dict['pages'] = page_list
    context_dict['user'] = request.user

    '''
        check if user has a profile?
    '''
    if request.user.is_authenticated:
        userprofile = UserProfile.objects.get(user=request.user)
        if userprofile.has_profile:
            context_dict['has_profile'] = True
        else:
            context_dict['has_profile'] = False


    # visits = request.session.get('visits')
    if 'visits' not in request.session:
        visits = 1
    else:
        visits = request.session['visits']

    reset_last_visit_time = False
   # last_visit = request.session.get('last_visit')

    if 'last_visit' in request.session:
        last_visit = request.session['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            reset_last_visit_time = True

    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits


    context_dict['visits'] = visits
    response = render(request,'rango/index.html',context_dict)

    return response


# -----------------------------------------******  Particular Category Page  ******-------------------------------------
def rango_categories(request, slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = slug)
        category.views = category.views + 1
        category.save()
        context_dict['category_name'] = category.name
        print(category.name)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['slug'] = slug

    except Category.DoesNotExist:
        '''
            We get here if we didn't find the specified category.
            Do not do anything - template displays the "no category" message for us.
        '''
        pass
    return render(request, 'rango/category.html',context_dict)


# ---------------------------------------------------******  About Page  ******-----------------------------------------
def rango_about(request):
    return render(request,'rango/about.html')


# --------------------------------------------------******  Add New Category  ******------------------------------------
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)
            print('form valid')
            return rango_index(request)
        else:
            print('form not valid')
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request,'rango/add_category.html',{'form': form})


# ---------------------------------------------------******  Add New Page  ******---------------------------------------
def add_page(request, slug):
    try:
        cat = Category.objects.get(slug = slug)
    except Category.DoesNotExist:
        cat = None
    print(cat)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if cat:
                print('formis fine')
                page = form.save(commit = False)
                page.category = cat
                page.views = 0
                page.save()
                return rango_categories(request, slug)
        else:
            print(form.errors)
    else:
        form = PageForm()
    return render(request,'rango/add_page.html',{'form': form, 'category' : cat, 'slug' : slug})


'''
    No need of this function now as now we are using registration_redux
'''
# --------------------------------------------------******  Register an User  ******------------------------------------
def register(request):

    '''
    Testing cookie 
    if request.session.test_cookie_worked():
        print('>>>>>>>>>>>>> TEST COOKIE WORKED!')
        request.session.delete_test_cookie()
    '''
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # hash the password with the set_password method.
            # once hashed we can update the user object
            user.set_password(user.password)
            user.save()

            # since we need to set the user attribute ourselves.
            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # save the userprofile model instance
            profile.save()

            registered  = True
            print('registered!!')

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',{'user_form' : user_form, 'profile_form' : profile_form,
                                                  'registered' : registered})


'''
    No need of this function now as now we are using registration_redux
'''
# --------------------------------------------------******  Login an User  ******---------------------------------------

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print('Invalid login details!')
            return HttpResponse('Invalid login details supplied')

    else:
        print()
        return render(request,'rango/login.html',{})


'''
    No need of this function now as now we are using registration_redux
'''
# -------------------------------------------------******  Logout an User  ******---------------------------------------
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


# -------------------------------------------------******  Restricted View  ******--------------------------------------
@login_required
def restricted(request):
    return HttpResponse('Since you are logged in, you can see this text!')


# ----------------------------------------------******  Build User Profile  ******--------------------------------------
@login_required
def build_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit = False)
            profile.user = request.user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.has_profile = True
            profile.save()
            print('>>>>>>>>>>>> Profile successfully built')

            return HttpResponseRedirect('/rango/')

        else:
            print(profile_form.errors)

    else:
        profile_form = UserProfileForm()

    return render(request, 'rango/profile.html', {'profile_form' : profile_form})


# ----------------------------------------------******  View User Profile  ******---------------------------------------
@login_required
def view_profile(request):
    user = request.user
    userprofile = UserProfile.objects.get(user = user)
    context_dict = {}
    if userprofile.picture:
        context_dict['picture'] = userprofile.picture
    if userprofile.website:
        context_dict['website'] = userprofile.website

    return render(request, 'rango/view_profile.html', context_dict)


# -----------------------------******  Track number of Times a Page has been visited ******-----------------------------
'''
    returns the the number of page views to ajax GET request. 
'''
def track_url(request):
    page_id = None
    url = '/rango/'
    views = 0
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id = page_id)
                page.views = page.views + 1
                views = page.views
                page.save()
                url = page.url
            except:
                pass
    return HttpResponse(views)


# -------------------------------------******  Like a Category ******---------------------------------------------------
@login_required
def like_category(request):
    category_id = None

    if request.method == 'GET':
        category_id = request.GET['category_id']

    category = Category.objects.get(id = category_id)
    likes = 0
    if category:
        category.likes = category.likes + 1
        likes = category.likes
        category.save()

    return HttpResponse(likes)


# -------------------------------------******  Suggest Categories ******------------------------------------------------
def gen_category_list(max_result = 0, starts_with = ''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith = starts_with)

    if cat_list and max_result > 0:
        if cat_list.count() > max_result:
            cat_list = cat_list[:max_result]

    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = gen_category_list(8, starts_with)

    #return render(request, 'rango/cat.html',{'cat_list' : cat_list})
    return HttpResponse(cat_list)






















