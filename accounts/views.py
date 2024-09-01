from django.shortcuts import render

# Create your views here.


def x(request):
    return render(request, 'x_page/x.html')
