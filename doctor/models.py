from django.db import models
from django.utils.html import mark_safe


def get_doctor_path(instance, file_name=None):
    return "media/doctors/{0}/{1}/{2}/{3}".format(
        instance.city,
        instance.expertise_category,
        instance.pk,
        file_name,
    )


def get_doctor_path_for_image(instance, file_name=None):
    return "media/doctors/{0}/{1}/{2}/{3}/{4}".format(
        instance.doctor.city,
        instance.doctor.expertise_category,
        instance.doctor.pk,
        instance.office_id,
        file_name,
    )


# Create your models here.
class Doctor(models.Model):

    # POST
    # https://nobat.ir/api/public/turn/daylist
    # body :
    # {
    #     nice_id: dr.maryam.motamedinasab
    #     office_id: 314150
    # }

    # POST
    # https://nobat.ir/api/public/turn/scheduleinfo
    # body :
    # {
    #     nice_id: dr.maryam.motamedinasab
    #     office_id: 314150
    #     day_key: 14030528
    # }

    # POST
    # https://nobat.ir/api/public/turn/doctor
    # body :
    # {
    #     nice_id: "dr.maryam.motamedinasab"
    # }

    # Site Meta Data
    data_drid = models.CharField(max_length=255, null=True, blank=True, unique=True) # OK!
    data_niceid = models.CharField(max_length=255, null=True, blank=True, unique=True) # OK!
    # data_officeid = models.CharField(max_length=255, null=True, blank=True)

    # Doctor data
    name = models.CharField(max_length=255) # OK!
    city = models.IntegerField()
    city_name = models.CharField(max_length=255)
    neighborhood = models.IntegerField(null=True, blank=True)
    neighborhood_name = models.CharField(max_length=255, null=True, blank=True)
    expertise_category = models.IntegerField()
    expertise_category_name = models.CharField(max_length=255, null=True, blank=True)
    expertise_name_1 = models.CharField(max_length=255) # OK!
    expertise_name_2 = models.CharField(max_length=255, null=True, blank=True) # OK!
    nezam_number = models.IntegerField() # OK!
    # appointment_type = models.CharField()
    education_level = models.CharField(max_length=255) # OK!
    is_verified = models.BooleanField(default=False) # OK!
    doctor_image = models.ImageField(upload_to=get_doctor_path, null=True, blank=True) # OK! BUT JUST URL
    like_count = models.IntegerField(default=0) # OK!
    comment_link = models.URLField(null=True, blank=True) # OK!

    extra_info = models.TextField(null=True, blank=True) # OK!
    office_data = models.JSONField(null=True, blank=True)
    comments_data = models.JSONField(null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True) # OK!

    # Meta data
    scraped_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    profile_url = models.URLField()
    source_page = models.TextField()

    def add_comment(self, star: int, text: str, date: str):
        json_comments = self.comments_data if self.comments_data else []
        new_comment = {
          "star": star,
          "text": text,
          "date": date,
        }
        json_comments.append(new_comment)
        self.comments_data = json_comments
        self.save()

    # POST
    # https://nobat.ir/api/public/doctor/office/tells
    # body :
    # {
    #     "office_id": "240915"
    # }
    def add_office_data(
            self,
            office_id: int, # Ok!
            office_type: str, # Ok!
            office_title: str, # Ok!
            office_city: str, # Ok!
            office_address: str, # Ok!
            office_description: str, # Ok!
            office_holiday: str, # Ok!
            office_phone: list[str],
            office_lat: str, # Ok!
            office_lon: str, # Ok!
    ):
        json_office = self.office_data if self.office_data else []
        new_office_data = {
            "office_type": office_type,
            "office_title": office_title,
            "office_city": office_city,
            "office_address": office_address,
            "office_description": office_description,
            "office_holiday": office_holiday,
            "office_phone": office_phone,
            "office_id": office_id,
            "office_lat": office_lat,
            "office_lon": office_lon,
        }

        # Append new entry to the list
        json_office.append(new_office_data)

        # Update the office_data field
        self.office_data = json_office

        # Save the model instance
        self.save()

    def get_doctor_profile_path(self):
        return get_doctor_path(self)

    def preview(self):
        try:
            return mark_safe(f'<img src = "{self.doctor_image.url}" style="max-width:100px; max-height:100px"/>')
        except Exception as e:
            return e.__str__()
        
    def __str__(self):
        return f'{self.name} {self.nezam_number}'


class Image(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_doctor_path_for_image, null=True, blank=True)
    office_id = models.IntegerField()

    def preview(self):
        try:
            return mark_safe(f'<img src = "{self.image.url}" style="max-width:200px; max-height:200px"/>')
        except Exception as e:
            return e.__str__()

    def __str__(self):
        return self.image.name


class Test(models.Model):
    text = models.TextField()


class ProfileUrlToScrape(models.Model):
    profile_url = models.URLField(unique=True)
    is_scraped = models.BooleanField(default=False)
    city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT,
        related_name='city_profiles_url_to_scrape',
        null=True,
        blank=True,
    )
    expertise_category = models.ForeignKey(
        'Speciality',
        on_delete=models.PROTECT,
        related_name='expertise_profiles_url_to_scrape',
        null=True,
        blank=True,
    )
    neighborhood = models.ForeignKey(
        'Neighborhood',
        on_delete=models.PROTECT,
        related_name='neighborhood_profiles_url_to_scrape',
        blank=True,
        null=True,
    )
    doctor = models.OneToOneField(
        Doctor,
        on_delete=models.SET_NULL,
        related_name='profiles_url_to_scrape',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.profile_url


class City(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name
