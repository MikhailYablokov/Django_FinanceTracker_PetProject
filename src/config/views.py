import locale
from datetime import datetime
from django.shortcuts import render




def invalid_page(request, exception):
    response = r'unknown_url.html'
    return render(request, response)