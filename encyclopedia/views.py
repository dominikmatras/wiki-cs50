from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
from .models import Entry
from markdown2 import markdown

def markdown_convert(title):
    markdowner = markdown(util.get_entry(title))
    if markdowner == None:
        return None
    else: 
        return markdowner
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error(request):
    return render(request, "encyclopedia/404.html")

def entries(request, title):
    if util.get_entry(title) is None:
        return redirect(reverse('error'))
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": markdown_convert(title)
    })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        if util.get_entry(query) is not None:
            content = markdown_convert(query)
            return render(request, "encyclopedia/entries.html", {
                "title":  query,
                "content": content
            })
        else: 
            entries = util.list_entries()
            recommend = []
            for entry in entries:
                if query.lower() in entry.lower():
                    recommend.append(entry)  
            return render(request, "encyclopedia/search.html", {
                "recommend": recommend
            })
            

