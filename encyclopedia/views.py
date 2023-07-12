from django.shortcuts import render, redirect
from django.urls import reverse
from . import util
from markdown2 import markdown
import random

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

def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "message": message
    })

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
            if recommend == []:
                return error(request, "Page not found")
            else: 
                return render(request, "encyclopedia/search.html", {
                    "recommend": recommend
                })

def new_page(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")
    else: 
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exist!"
            })
        else: 
            util.save_entry(title, content)
            content_html = markdown_convert(title)
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "content": content_html
                 })

def edit(request):
    if request.method == 'POST':
        title = request.POST['page_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        content_html = markdown_convert(title)
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": content_html
        })
    
def random_page(request):
    allEntries = util.list_entries()
    title = random.choice(allEntries)
    content = markdown_convert(title)
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": content
    })