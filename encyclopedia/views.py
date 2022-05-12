from logging import PlaceHolder
from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from django.utils.safestring import mark_safe

from . import util

class SearchForm(forms.Form):
    search_term = forms.CharField(label="Search")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="")
    content = forms.CharField(label="", widget=forms.Textarea)

def index(request):
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
        "title": name,
        "content": content,
        "form": SearchForm()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data["search_term"]
            if search_term in util.list_entries():
                markdowner = Markdown()
                return render(request, "encyclopedia/entry.html", {
                   "content": markdowner.convert(util.get_entry(search_term)),
                   "form": SearchForm()
                })
            else:
                entries = util.list_entries()
                entry_list = []
                for entry in entries:
                    if search_term in entry:
                        entry_list.append(entry)
                return render(request, "encyclopedia/search_results.html", {
                    "entries": entry_list,
                    "form": SearchForm()
                })

def new(request):
    return render(request, "encyclopedia/new.html", {
        "new_form": NewEntryForm(),
        "form": SearchForm()
    })

def save(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                markdowner = Markdown()
                return render(request, "encyclopedia/entry.html", {
                    "content": markdowner.convert(util.get_entry(title)),
                    "form": SearchForm()
            })
            else:
                return render(request, "encyclopedia/entry.html", {
                    "content": "Error. This title already exists",
                    "form": SearchForm()
                 })