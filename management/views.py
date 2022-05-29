from django.shortcuts import render, redirect

from .models import *
from .forms import *
# .FORMS REFERS TO THE FORMS.PY IN CURRENT DIRECTORY AND * USED FOR IMPORTING EVERYTHING

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

# HOME PAGE
def index(request):
    return render(
        request,
        'index.html',
    )


def ItemListView(request):
    item_list = Item.objects.all()

    return render(request, 'catalog/item_list.html', locals())

@login_required
def Customer_OrderListView(request):
    customer = Customer.objects.get(cust_id=request.user)
    ord = Order.objects.filter(name=customer)
    order_list=[]
    for o in ord:
        order_list.append(o.item)
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'catalog/item_list.html', locals())

def ItemDetailView(request, pk):
    item = get_object_or_404(Item, id=pk)
    price = Item.objects.filter(item=item).exclude(price="none")
    try:
        cust = Customer.objects.get(price=request.user)
        pr= Item.objects.get(price="none")
    except:
        pass
    return render(request, 'catalog/item_detail.html', locals())



@login_required
def ItemCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def ItemUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Item.objects.get(id=pk)
    form = ItemForm(instance=obj)
    if request.method == 'POST':
        form = ItemForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def ItemDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Item, pk=pk)
    obj.delete()
    return redirect('index')



@login_required
def Customer_Order_Issue(request, pk):
    obj = Item.objects.get(id=pk)
    cust = Customer.objects.get(cust_id=request.user)
    s = get_object_or_404(Customer, cust_id=str(request.user))
    if s.total_Order > 0:
        message = "Order has been issued."
        a = Order()
        a.customer = s
        a.item = obj
        a.issue_date = datetime.datetime.now()
        obj.save()
        cust.total_Order=cust.total_Order+1
        cust.save()
        a.save()
    else:
        message = "Please add an item in cart."
    return render(request, 'catalog/result.html', locals())


@login_required
def CustomerCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            s=form.cleaned_data['cust_id']
            form.save()
            u=User.objects.get(username=s)
            s=Customer.objects.get(cust_id=s)
            u.email=s.email
            u.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def CustomerUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Customer.objects.get(id=pk)
    form = CustomerForm(instance=obj)
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def CustomerDelete(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    obj.delete()
    return redirect('index')

@login_required
def CustomertList(request):
    customer = Customer.objects.all()
    return render(request, 'catalog/customer_list.html', locals())

@login_required
def CustomerDetail(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    items = Order.objects.filter(customer=customer)
    return render(request, 'catalog/customer_detail.html', locals())




@login_required
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Order.objects.get(id=pk)
    item_pk=obj.item.id
    customer_pk=obj.customer.id
    customer = Customer.objects.get(id=customer_pk)
    customer.total_Order=customer.total_Order-1
    customer.save()

    item = Item.objects.get(id=item_pk)
    item.save()
    obj.delete()
    return redirect('index')


import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
def search_item(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'category', 'price'])

        item_list= Item.objects.filter(entry_query)

    return render(request,'catalog/item_list.html',locals() )
def search_customer(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['roll_no','name','email'])

        customer = Customer.objects.filter(entry_query)

    return render(request,'catalog/customer_list.html',locals())


