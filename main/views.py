from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ItemForm
from django.contrib import messages
from .models import Item
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group 

# Create your views here.
@login_required(login_url='login')
@admin_only
def index(request):
    obj=Item.objects.all()
    if request.POST:
        str_date=request.POST.get('filterdate')
        # print(str_date)
        # print(type(str_date))
        py_date=datetime.datetime.strptime(str_date,"%Y-%m-%d")
        # dt=date(fdate.year,fdate.month,fdate.day)
        obj=Item.objects.filter(date=py_date)
    #form=ItemForm(request.POST)
    #for p in Item.objects.raw("SELECT id,itemname,itemquantity,itemstatus FROM calc_Item WHERE date='%d/%m/%Y'",[dtime]):
    #context={'items':items}
    return render(request,'index.html',{'obj':obj})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add(request):
    #dest=ItemForm()
    # additem=Item.objects.all()
    if request.method == 'POST':
        form=ItemForm(request.POST)
        #print(form)
        if form.is_valid():
            form.save()
            messages.success(request,"Item has been added")
        else:
            messages.error(request,"Item has NOT been added")
            print(form.errors)
    # else:
    #     form = ItemForm()
    return render(request,'add.html')
    # return render(request,'add.html',{"Item":additem})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update(request, item_id):
    try:
        item_to_be_updated=get_object_or_404(Item, pk=item_id)
        if request.method == 'POST':
            # item_id = request.POST["item"]
            form=ItemForm(request.POST,instance=item_to_be_updated)
            if form.is_valid():
                form.save()
                messages.success(request,"Record updated Successfully")
        status_choices = ["PENDING","BOUGHT","NOT AVAILABLE"]
        return render(request,'update.html', {"item_to_be_updated":item_to_be_updated, "status_choices":status_choices})
    except:
        return redirect("index")

# def updaterecord(request,item_id):
#
#     return redirect('/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete(request,item_id):
    #obj=Item.objects.all()
    obj=Item.objects.filter(pk=item_id).delete()
    #item_to_be_deleted=objects.filter(Item, pk=item_id)
    
    # form=ItemForm(request.POST,instance=item_to_be_deleted)
    # form.delete()
    #messages.success(request,"Record deleted Successfully")
    return redirect("index")
