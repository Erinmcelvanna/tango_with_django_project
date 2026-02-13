from django.shortcuts import render
from rango.models import Category, Page
from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict={'categories':category_list, 'pages':page_list,}
    return render(request, 'rango/index.html',context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['category'] = category
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

def goto(request):
    page_id = None
    url = ''

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    if url:
        return redirect(url)
    else:
        return redirect('/rango/')
