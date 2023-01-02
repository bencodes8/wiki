from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import choice

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
        "random" : choice(util.list_entries())
    })

def search(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "info": util.get_entry(title),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
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
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": new_entry["page"]}))
                    
    return render(request, "encyclopedia/create.html", {
        "form": NewCreateForm()
    })
    
def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            edited_page = form.cleaned_data
            util.save_entry(title, edited_page["new_description"])
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": title}))
            
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditForm({'new_description': util.get_entry(title)})
    })

def random(request):
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": choice(util.list_entries())}))

        
    
