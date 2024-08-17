from django.contrib import admin
from .models import (
    Doctor,
    Image,
    Test,
    ProfileUrlToScrape,
    City,
    Speciality,
    Neighborhood,
)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_name', 'expertise_name_1', 'education_level', 'is_verified')
    search_fields = ('name', 'city_name', 'expertise_name_1', 'education_level')
    list_filter = ('is_verified', 'expertise_category', 'city')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'preview')
    search_fields = ('doctor__name',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        return obj.preview()
    preview.short_description = 'Image Preview'
    preview.allow_tags = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('pk',)


@admin.register(ProfileUrlToScrape)
class ProfileUrlToScrapeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'profile_url',
        'is_scraped',
        'city',
        'expertise_category',
    )
    list_filter = ('is_scraped', 'city', 'expertise_category')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    list_filter = ('name',)
    search_fields = ('name', 'number')


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    list_filter = ('name',)
    search_fields = ('name', 'number')


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    list_filter = ('name',)
    search_fields = ('name', 'number')

