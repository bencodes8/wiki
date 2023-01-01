from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util

class NewCreateForm(forms.Form):
    page = forms.CharField(label="New Page Title")
    description = forms.CharField(widget=forms.Textarea(), label="")
    

def index(request):
    if request.method == "POST":
        found = []
        for entry in util.list_entries():
            if entry.lower().find(request.POST["q"].lower()) != -1:
                index = util.list_entries().index(entry)
                found += [util.list_entries()[index]]
                return render(request, "encyclopedia/index.html", {
                    "entries": found
                })
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()  
    })

def create(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data
            print(util.list_entries())
            for entry in util.list_entries():
                if entry.lower() == new_entry["page"].lower():
                    return render(request, "encyclopedia/create.html", {
                        "page": new_entry["page"],
                        "error": True
                    })
                else:
                    util.save_entry(new_entry["page"], new_entry["description"])
                    
                    
    return render(request, "encyclopedia/create.html", {
        "form": NewCreateForm()
    })

def entry(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "info": util.get_entry(title),
            "title": title.upper()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "url_error": True
        })
        
    
