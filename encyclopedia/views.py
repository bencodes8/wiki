from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import choice
import markdown2

from . import util

# class to create a form 
class NewCreateForm(forms.Form):
    page = forms.CharField(label="New Page Title")
    description = forms.CharField(widget=forms.Textarea(), label="")

# class to create another form for editing entries 
class EditForm(forms.Form):
    new_description = forms.CharField(widget=forms.Textarea(), label="")

'''
    index function:
    ~POST~
    - users can search pages given a substring of the title of the page
    - if no pages are found, a message will show 
    - else display all pages on current page
    
    -display all entry pages
    
'''
def index(request):
    if request.method == "POST":
        found = []
        for entry in util.list_entries():
            if entry.lower().find(request.POST["q"].lower()) != -1:
                index = util.list_entries().index(entry)
                # appends pages to list if search query is found
                found += [util.list_entries()[index]]
        return render(request, "encyclopedia/index.html", {
            "entries": found
        })
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random" : choice(util.list_entries())
    })

'''
    entry function:
    - the route will direct the user based on the title of the route
    - if the user inputs a title that exists in the entry list, direct the user to the page
    - else return an error page
'''
def entry(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "info": markdown2.markdown(util.get_entry(title)),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
'''
    create function:
    ~ POST ~
    - user can create a new page by inputting a title and description
    - if title of page exists, reject it, redirect user back to the create page, and return an error message
    - else save the new page and redirect user to new page
    - the new page should also now be added on the index page
'''
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

'''
    edit function:
    ~ POST ~
    - users can edit a page
    - for QOL, the entry description will already prepopulate the textarea
    - save entry
    - the user will be redirected to the newly edited page
'''
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

'''
    /random route
    redirects user to random entry page
'''
def random(request):
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title": choice(util.list_entries())}))

        
    
