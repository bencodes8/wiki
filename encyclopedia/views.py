from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
import random

from . import util

class NewCreateForm(forms.Form):
    page = forms.CharField(label="New Page Title")
    description = forms.CharField(widget=forms.Textarea(), label="")

class EditForm(forms.Form):
    new_description = forms.CharField(widget=forms.Textarea(), label="")

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
        "entries": util.list_entries(),
        "random": random.choices(util.list_entries()).pop()
    })

def search(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "info": util.get_entry(title),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "url_error": True,
            "title": title
        })

def create(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data
            
            for entry in util.list_entries():
                if entry.lower() == new_entry["page"].lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": NewCreateForm(),
                        "page": new_entry["page"],
                        "error": True
                    })
            util.save_entry(new_entry["page"], new_entry["description"])
            return redirect(f'/wiki/{new_entry["page"]}')
                    
    return render(request, "encyclopedia/create.html", {
        "form": NewCreateForm()
    })
    
def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            edited_page = form.cleaned_data
            print(edited_page["new_description"])
            util.save_entry(title, edited_page["new_description"])
            return redirect(f'/wiki/{title}')
            
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditForm({'new_description': util.get_entry(title)})
    })


        
    
