from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.routers import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
import datetime

class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            instanse = Order.objects.get(id=serializer.data['id'])
            a = instanse.code_generatsion
            result = {
                "code": a
            }
            return Response({"code": result})
        return Response({"status": "Error!"})
    def retrieve(self, request, *args, **kwargs):
        order_all = self.queryset.filter(code = kwargs["pk"])
        serializer = OrderSerializer(order_all,many=True)
        return Response(serializer.data)


class PassangerView(ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassangerSerializer

    def update(self, request, *args, **kwargs):
        """Tasdiqlash bulsa kamaytiradigan funksiya"""
        # print(request.data,kwargs)
        idd = kwargs["pk"]
        obb = Passenger.objects.filter(id=idd)
        if request.data["user_status"] == "Tasdiqlangan":
            user_driver = Order.objects.filter(id=request.data["driver"])
            quantity = user_driver.values_list("number_of_vacancies")[0][0]
            if int(user_driver.values_list("number_of_vacancies")[0][0]) > 0:
                quantity -= 1
                user_driver.update(number_of_vacancies=quantity)
                obb.delete()
            else:
                user_driver.delete()
                return Response({"status":"Update bo'lmadi"})

        return Response({"status":"Update bo'ldi"})
    def retrieve(self, request, *args, **kwargs):
        """
        Driverni ID si orqali Yo'lovchilarni chiqarib beradi
        """
        id = kwargs["pk"]
        a = Passenger.objects.filter(driver=id)
        serilizer = self.get_serializer(a, many=True)
        return Response(serilizer.data)


class OrderFilterView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSearchSerializer

    def create(self, request, *args, **kwargs):
        """
        Yo'nalish bo'yicha va jo'nab ketish vaqti bo'yicha
        Filter qilishimizda foydalanamiz
        """
        year = request.data["departure_time"][:4]
        month = request.data["departure_time"][5:7]
        day = request.data["departure_time"][8:10]
        time_now = datetime.datetime.now().date()
        # malumotlarni tozalab turadigan algoritm
        for i in self.queryset:
            print(i.departure_time.date(),time_now)
            if i.departure_time.date() and i.departure_time.date() <= time_now:
                try:
                    i.delete()
                except Exception as e:
                    print(e)
        result = self.queryset.filter(departure_station=request.data["departure_station"]).filter(
            arrival_station=request.data["arrival_station"]).filter(departure_time__year=year).filter(
            departure_time__month=month).filter(departure_time__day=day)
        data = []
        for j in result:
            a = data.append({
                "id":j.id,
                "full_name":j.full_name,
                "phone_number":j.phone_number,
                "telegram_akkount":j.telegram_akkount,
                "add_date":j.add_date,
                "about_car":j.about_car,
                "departure_station":j.departure_station,
                "arrival_station":j.arrival_station,
                "departure_time":j.departure_time,
                "number_of_vacancies":j.number_of_vacancies,
                "sex":j.sex,
                "price":j.price,
                "car_picture": j.car_picture,
                "description": j.description,
            })
            data.append(a)
        datas = []
        for item in data:
            if item:
                datas.append(item)
        print(datas)
        serializer = OrderSerializer(datas,many=True)
        return Response(serializer.data)

class PassangerStatusView(ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassangerStatusSerializer
    def create(self, request, *args, **kwargs):
        status = request.data["user_status"]
        print(request.data)
        if status == "Tasdiqlangan":
            instance = Passenger.objects.get(pk =request.data["id"])
            print(instance)
            self.perform_destroy(instance)
        return Response({"status":"O'chirildi"})
    def destroy(self, request, *args, **kwargs):
        # status = request.data["user_status"]
        print(request.data,args,kwargs)
        # if status == "Tasdiqlangan":
        #     a = Order.objects.get("number_of_vacancies")
        #     print(a)
        #     instance = Passenger.objects.get(pk =kwargs["pk"])
        #     print(instance)
        #     # self.perform_destroy(instance)
        return Response({"status":"O'chirildi"})

# class CodeFilterView(ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     def retrieve(self, request, *args, **kwargs):
#         code = kwargs["pk"]
#

