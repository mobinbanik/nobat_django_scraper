import requests
import bs4
import undetected_chromedriver
from .models import Doctor


def get_comments(text):
    pass


def scrape(text) -> dict[str, str]:
    soup = bs4.BeautifulSoup(text, 'html.parser')
    # print(soup)

    name = soup.find('h1', attrs={'class': 'doctor-ui-name'})
    is_verified = False
    if name.find('img'):
        is_verified = True
    name = name.find('span').text

    _specialties = soup.find_all('h2', attrs={'class': 'doctor-ui-specialty'})
    specialties = list()

    for specialty in _specialties:
        specialties.append(specialty.text)

    doctor_code_tag = soup.find('div', attrs={'class': 'doctor-code'}).find_all('span')
    doctor_code = doctor_code_tag[1].text
    education_level = doctor_code_tag[0].text

    doctor_image_profile = soup.find('div', attrs={'class': 'doctor-ui-profile'})
    doctor_image_profile = doctor_image_profile.find('img')
    doctor_image_url = doctor_image_profile['src']
    like_count = soup.find('span', attrs={'id': 'followers-count'}).text

    comment_link = soup.find('a', attrs={'class': 'btn btn-rounded btn-gray'})
    comment_link = comment_link['href']

    extra_info_tag = soup.find('p', attrs={'class': 'nl-to-br'})
    extra_info = str()
    for info in extra_info_tag:
        extra_info += info.text

    temp = Doctor.objects.create(
        name=name,
        is_verified=is_verified,
    )
    return {
        'extra_info': extra_info,
        'comment_link': comment_link,
        'like_count': like_count,
        'doctor_image_url': doctor_image_url,
        'doctor_code': doctor_code,
        'education_level': education_level,
        'name': name,
        'is_verified': is_verified,
        'specialties': specialties,
    }


def main():
    with open('../3_off.html', 'r', encoding='utf-8') as f:
        text = f.read()
    scrape(text)


if __name__ == '__main__':
    main()