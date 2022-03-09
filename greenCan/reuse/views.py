from django.shortcuts import render
from .forms import FormPost
from .models import Post

def donation_view(request):
    template = "donate-item-page.html"
    context = {"is_reuse": True}
    return render(request, template, context=context)

def ShowAdPostForm(request):
    form= FormPost(request.POST or None)
    if form.is_valid():
        form.save()
        
    context= {'form': form }
        
    return render(request, 'adpostui.html', context)

def showdata(request):
 
    alldata= Post.objects.all()
    
    context= {'alldata': alldata}

        
    return render(request, 'adpostuidata.html', context)

