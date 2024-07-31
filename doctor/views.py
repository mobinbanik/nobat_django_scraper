from django.http import HttpResponse
from django.shortcuts import render
from .scraper import scrape, main
from .models import Doctor, Image, Test


# Create your views here.
def run_scraper(requests):
    text = Test.objects.all()[0].text
    scraper = scrape(text)
    te = '<meta charset="UTF-8">'
    text = str()
    for item in scraper.items():
        text = text + str(item)
        text += '<br>'

    return HttpResponse(te + str(text), content_type='text/html')