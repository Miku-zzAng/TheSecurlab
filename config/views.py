from django.shortcuts import render, redirect

def index(request):
        context = {
                "user":request.user
        }
        return render(request, "index.html")