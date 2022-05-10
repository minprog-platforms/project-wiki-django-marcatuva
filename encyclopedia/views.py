from django import forms
from django.shortcuts import render
from markdown2 import Markdown

from . import util

class SearchForm(forms.Form):
    search_term = forms.CharField(label="Search")

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data["search_term"]
            print(search_term)
            if search_term in util.list_entries():
                return render(request, "encyclopedia/entry.html", {
                "content": util.get_entry(name)
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, name):
    markdowner = Markdown()
    entry = util.get_entry(name)
    if entry == None:
        content = entry
    else:
        content = markdowner.convert(entry)
    return render(request, "encyclopedia/entry.html", {
        "content": content
    })

# def search(request):
    

