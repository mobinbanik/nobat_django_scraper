import os
import subprocess
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .scraper import scrape, main, download_image_and_save_to_model, download_gallery_for_model
from .models import Doctor, Image, Test, City, Speciality, Neighborhood, ProfileUrlToScrape
from doctor.csv_manager import csv_get_all_rows, csv_append
from doctor.Logger.Logger import log_message


def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors_list.html', {'doctors': doctors})


def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_profile.html', {'doctor': doctor})


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
    # cities = os.listdir(base_path_list_profile)
    # for city in cities:
    #     log_message(extract_city_number(city), f'{city} strated', '--STARTED--', level='INFO')
    #     current_directory = os.path.join(base_path_list_profile, city)
    #     csv_list = os.listdir(current_directory)
    #     for csv in csv_list:
    #         profiles = csv_get_all_rows(os.path.join(current_directory, csv))
    #         create_profiles(profiles, extract_city_number(city), extract_expert_number(csv))
    # profiles = None
    text = Test.objects.all()[0].text
    city = City.objects.all()[0]
    expertise = Speciality.objects.all()[0]

    json_data = scrape(text)
    doctor = Doctor.objects.create(
        data_drid=json_data['data_drid'],
        data_niceid=json_data['data_niceid'],
        name=json_data['name'],
        city=city.number,
        city_name=city.name,
        expertise_category=expertise.number,
        expertise_category_name=expertise.name,

        expertise_name_1=json_data['specialties1'],
        expertise_name_2=json_data['specialties2'],
        nezam_number=json_data['doctor_code'],
        education_level=json_data['education_level'],
        is_verified=json_data['is_verified'],
        # doctor_image=json_data['education_level'],
        like_count=json_data['like_count'],
        comment_link=json_data['comment_link'],

        extra_info=json_data['extra_info'],
        office_data=json_data['offices'],
        comments_data=json_data['comments'],
        social_media=json_data['social_media'],

        # Meta data
        profile_url = 'url',
        source_page = text,
    )
    download_image_and_save_to_model(
        json_data['doctor_image_url'],
        doctor,
        'doctor_image',
    )
    for office in json_data['offices']:
        for url in office['_office_gallery']:
            image = Image.objects.create(
                doctor=doctor,
                office_id=office['office_id'],
            )
            download_gallery_for_model(
                url,
                image,
                'image',
            ) 
    return HttpResponse('Done!')


