from django.shortcuts import render
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
    # def retrieve(self, request, *args, **kwargs):
    #     print(request.data)
    #     year,month,day = request.data["time"]
    #
    #     order_all = Order.objects.filter()


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
            if i.departure_time.date() <= time_now:
                i.delete()
        result = self.queryset.filter(departure_station=request.data["departure_station"]).filter(
            arrival_station=request.data["arrival_station"]).filter(departure_time__year=year).filter(
            departure_time__month=month).filter(departure_time__day=day)
        serializer = self.get_serializer(result, many=True)

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
