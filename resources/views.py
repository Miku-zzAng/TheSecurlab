from django.shortcuts import render

def share(request):
    return render(request, "resources/share.html")