from django.db import models
from django.contrib.auth.models import User
import random

word = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
        "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z",
        "X", "C", "V", "B", "N", "M", "1", "2", "3", "4",
        "5", "6", "7", "8", "9", "0", ]


class Order(models.Model):
    jinsi = {
        ("Erkak", "Erkak"),
        ("Ayol", "Ayol"),
        ("Ixtiyoriy", "Ixtiyoriy"),
    }
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13)  # +998990010101
    telegram_akkount = models.CharField(max_length=300)  # https://t.me/Poputni_uz
    add_date = models.DateTimeField(auto_now_add=True,blank=True)
    about_car = models.CharField(max_length=1000,blank=True)
    departure_station = models.CharField(max_length=200)  # jo'nab ketish bekati
    arrival_station = models.CharField(max_length=200)  # yetib borish bekati
    departure_time = models.DateTimeField(null=True)  # jo'nab ketish vaqti
    number_of_vacancies = models.IntegerField(default=1,null=True)  # bo'sh o'rinlar soni
    sex = models.CharField(max_length=50, default="Ixtiyoriy", choices=jinsi)
    price = models.CharField(max_length=200)
    car_picture = models.ImageField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=6, default="000000", null=True, blank=True)
    edited_date = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    longitude = models.CharField(max_length=40, null=True,blank=True)
    latitude = models.CharField(max_length=40, null=True,blank=True)

    def __str__(self):
        try:
            return self.full_name
        except:
            return ""

    @property
    def image_URL(self):
        try:
            return self.car_picture.url
        except:
            return ""

    @property
    def code_generatsion(self):  # Kod generatsiya qiberadigan funksiya
        code = ""
        for i in range(6):
            code += random.choice(word)
        self.code = code
        # print(code)
        self.save()
        return code
    @property
    def edit_date(self):
        self.edited_date = self.edited_date
        self.save()


class Passenger(models.Model):
    status = {
        ("Tasdiqlangan", "Tasdiqlangan"),
        ("Tasdiqlanmagan", "Tasdiqlanmagan"),
    }
    driver = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13)
    tg_akkount = models.CharField(max_length=30, null=True,blank=True)
    add_date = models.DateTimeField(auto_now_add=True,blank=True)
    user_status = models.CharField(max_length=40, default="Tasdiqlanmagan", choices=status)

    def __str__(self):
        return self.full_name
