import requests
import bs4
import undetected_chromedriver
from .models import Doctor


def get_comments(text):
    # TODO get comments
    pass


def parse_office(text: str, office_type: str):
    soup = bs4.BeautifulSoup(text, 'html.parser')

    _office_id = soup.find('div', attrs={'class': 'office'})
    if _office_id:
        _office_id = _office_id['data-officeid']

    if office_type == 'visicall':
        return {
            'office_type': office_type,
            'office_id': _office_id,
        }

    _office_title = soup.find('strong', attrs={'class': 'office-title'})
    if _office_title:
        _office_title = _office_title.text

    _office_city_address_tag = soup.find('div', attrs={'class': 'office-address'})
    _office_city = None
    _office_address = None
    if _office_city_address_tag:
        _office_city_address_tag = _office_city_address_tag.find_all('strong')
        _office_city = _office_city_address_tag[0].text
        _office_address = _office_city_address_tag[1].text

    _office_description = soup.find('div', attrs={'class': 'office-description'})
    if _office_description:
        _office_description = _office_description.text

    _office_holiday = soup.find('div', attrs={'class': 'office-holiday'})
    if _office_holiday:
        _office_holiday = _office_holiday.text

    _office_map_tag = soup.find('div', attrs={'class': 'office-map-container'})
    _office_lat = None
    _office_lon = None
    if _office_map_tag:
        _office_map_tag = _office_map_tag.find('div')
        _office_lat = _office_map_tag['data-lat']
        _office_lon = _office_map_tag['data-lng']

    return {
        'office_type': office_type,
        'office_id': _office_id,
        'office_title': _office_title,
        'office_city': _office_city,
        'office_address': _office_address,
        'office_description': _office_description,
        'office_holiday': _office_holiday,
        'office_lat': _office_lat,
        'office_lon': _office_lon,
    }


def scrape(text) -> dict[str, str]:
    soup = bs4.BeautifulSoup(text, 'html.parser')
    # print(soup)
    # -\/-
    _data = soup.find('div', attrs={'id': 'doctor'})
    _data_drid = None
    _data_niceid = None
    if _data:
        _data_drid = _data['data-drid']
        _data_niceid = _data['data-niceid']

    # -\/-
    _name = soup.find('h1', attrs={'class': 'doctor-ui-name'})
    _is_verified = None
    if _name:
        if _name.find('img'):
            _is_verified = True
        else:
            _is_verified = False
        _name = _name.find('span').text

    # -\/-
    offices = soup.find_all('div', attrs={'class': 'office'})
    offices_json_list = list()
    if offices:
        for office in offices:
            office_type = 'normal'
            if 'hide' in office['class']:
                office_type = 'visicall'
            json_data = parse_office(str(office), office_type)
            offices_json_list.append(json_data)
    # TODO get phone number and parse it
    # -\/-
    _nezam_number_tag = soup.find('div', attrs={'class': 'doctor-code'})
    _doctor_code = None
    _education_level = None
    if _nezam_number_tag:
        _nezam_number_tag = _nezam_number_tag.find_all('span')
        _doctor_code = _nezam_number_tag[1].text
        _education_level = _nezam_number_tag[0].text

    # -\/-
    _doctor_image_profile = soup.find('div', attrs={'class': 'doctor-ui-profile'})
    if _doctor_image_profile:
        _doctor_image_profile = _doctor_image_profile.find('img')
        _doctor_image_profile = _doctor_image_profile['src']

    # -\/-
    _like_count = soup.find('span', attrs={'id': 'followers-count'})
    if _like_count:
        _like_count = _like_count.text

    # -\/-
    _comment_link = soup.find('a', attrs={'class': 'btn btn-rounded btn-gray'})
    if _comment_link:
        _comment_link = _comment_link['href']

    # -\/-
    extra_info_tag = soup.find('p', attrs={'class': 'nl-to-br'})
    _extra_info = str()
    if extra_info_tag:
        for info in extra_info_tag:
            _extra_info += info.text

    # -\/-
    _social_media_tag = soup.find('div', attrs={'class': 'social-media'})
    _social_media = list()
    if _social_media_tag:
        _social_media_tag = _social_media_tag.find_all('a')
        for a in _social_media_tag:
            _social_media.append(a['href'])

    # -\/-
    _expertise = soup.find_all('h2', attrs={'class': 'doctor-ui-specialty'})
    _expertise_name_1 = None
    _expertise_name_2 = None
    if _expertise:
        _expertise_name_1 = _expertise[0].text
        if len(_expertise) > 1:
            _expertise_name_2 = _expertise[1].text

    # temp = Doctor.objects.create(
    #     name=name,
    #     is_verified=is_verified,
    #
    # )
    return {
        'extra_info': _extra_info,
        'comment_link': _comment_link,
        'like_count': _like_count,
        'doctor_image_url': _doctor_image_profile,
        'doctor_code': _doctor_code,
        'education_level': _education_level,
        'name': _name,
        'is_verified': _is_verified,
        'specialties1': _expertise_name_1,
        'specialties2': _expertise_name_2,
        'data_drid': _data_drid,
        'data_niceid': _data_niceid,
        'offices': offices_json_list,
        'social_media': _social_media,
    }



def main():
    with open('../3_off.html', 'r', encoding='utf-8') as f:
        text = f.read()
    scrape(text)


if __name__ == '__main__':
    main()