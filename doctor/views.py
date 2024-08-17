import os
import subprocess
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .scraper import scrape, main
from .models import Doctor, Image, Test, City, Speciality, Neighborhood, ProfileUrlToScrape
from doctor.csv_manager import csv_get_all_rows, csv_append
from doctor.Logger.Logger import log_message

# Create your views here.
def run_scraper(requests):
    text = Test.objects.all()[0].text
    scraper = scrape(text)
    return JsonResponse(scraper, safe=False)
    # te = '<meta charset="UTF-8">'
    # text = str()
    # for item in scraper.items():
    #     text = text + str(item)
    #     text += '<br>'
    #
    # return HttpResponse(te + str(text), content_type='text/html')


def extract_city_number(city):
    return city.split('-')[1]


def extract_expert_number(expert):
    return expert.split('.')[0].split('_')[1].split('-')[1]


def create_profiles(profiles, city_number, expert_number):
    log_message(f'city: {city_number}', f'expert: {expert_number}', '--start_saving_csv--', level='INFO')
    for profile in profiles:
        try:
            if len(profile) == 0:
                continue
            if '/doctor/' in profile[0][:10]:
                continue

            ProfileUrlToScrape.objects.get_or_create(
                profile_url=profile[0],
                city=City.objects.get(number=city_number),
                expertise_category=Speciality.objects.get(number=expert_number),
            )
            log_message(f'url: {profile}', f'created', '--CREATED--', level='INFO')
        except Exception as e:
            log_message(f'url: {profile}', f'{e.__str__()}', '--ERROR--', level='ERROR')


def pwd(requests):
    base_path_data = 'data'
    base_path_list_profile = 'data\\profile list'
    cities = os.listdir(base_path_list_profile)
    for city in cities:
        log_message(extract_city_number(city), f'{city} strated', '--STARTED--', level='INFO')
        current_directory = os.path.join(base_path_list_profile, city)
        csv_list = os.listdir(current_directory)
        for csv in csv_list:
            profiles = csv_get_all_rows(os.path.join(current_directory, csv))
            create_profiles(profiles, extract_city_number(city), extract_expert_number(csv))
    profiles = None

    return HttpResponse(current_directory + '<br>' + str(cities))


