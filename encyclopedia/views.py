from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "info": util.get_entry(title),
            "title": title.title()
        })
    return render(request, "encyclopedia/error.html", {
        "title": title
    })

