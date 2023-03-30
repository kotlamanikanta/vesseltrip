from django.shortcuts import render
from pymongo import MongoClient
from datetime import datetime, timedelta
from django.http import HttpResponse
from bson.json_util import dumps
from bson.objectid import ObjectId
import csv
from django.http import HttpResponse

connection = MongoClient()
db = connection.querydata
# Create your views here.


def homepage(request):
    return render(request, "index.html")


def get_sensor_data(request):

    trip_id = "63d4228e01afc1d6b6813e38"
    sensor_name = "GPS"
    from_time = datetime.now() - timedelta(days=90)
    to_time = datetime.now()
    sensor_data = db.vesseltripdata.aggregate(
        [
            {
                "$match": {
                    "dateTime": {"$gte": from_time, "$lte": to_time},
                    "tripId": trip_id,
                    "sensorName": sensor_name,
                }
            },
            {"$project": {"_id": 0}},
        ]
    )
    data = list(sensor_data)
    # print(data,"abcd")
    # this function used to convert the html display data to csv formate
    if request.GET.get("export", None) == "True":
        r = some_view(data)
        return r
    return render(request, "get_sensor_data.html", {"data": data})


def timespan(request):

    trip_id = "63d4228e01afc1d6b6813e38"
    sensor_name = "GPS"
    from_time = datetime.now() - timedelta(days=90)
    to_time = datetime.now()
    sensor_data = db.vesseltripdata.aggregate(
        [
            {
                "$match": {
                    "dateTime": {"$gte": from_time, "$lte": to_time},
                    "sensorName": sensor_name,
                }
            },
            {"$project": {"_id": 0}},
        ]
    )
    # print(sensor_data)
    d = list(sensor_data)
    # print("hi")
    print(d, "hi")
    if request.GET.get("export", None) == "True":
        r = some_view(d)
        return r
    return render(request, "Timedata.html", {"dm": d})


# get_sensor_data(sensor_name,from_time,to_time,trip_id)

# 3] From a given trip, give the sum of "Sensor X" throughout the entire trip
def sensor_data(request):
    trip_id = "63d4228e01afc1d6b6813e38"
    sensor_name = "GPS"
    # from_time=datetime.now()-timedelta(days=90)
    # to_time=datetime.now()
    sensor_sum_data = db.vesseltripdata.aggregate(
        [
            {"$match": {"tripId": trip_id, "sensorName": sensor_name}},
            {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
            {
                "$group": {
                    "_id": "$sensorName",
                    "index0_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 0]}},
                    "index1_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 1]}},
                    "index2_sum": {"$sum": {"$arrayElemAt": ["$dataPoints", 2]}},
                }
            },
        ]
    )
    # print(sensor_sum_data)
    d = list(sensor_sum_data)
    if request.GET.get("export", None) == "True":
        r = some_view(d)
        return r
    # print(type(sensor_sum_data))
    # print(dumps(list(sensor_sum_data)))
    # return HttpResponse("mani")
    return render(request, "sensor_data.html", {"mk": d})


# get_sensor_data_sum(sensor_name,trip_id)

# 4] From a given trip, give the average of "Sensor X" throughout the entire trip
def sensor_data_avg(request):
    trip_id = "63d4228e01afc1d6b6813e38"
    sensor_name = "GPS"
    # from_time=datetime.now()-timedelta(days=90)
    # to_time=datet ime.now()
    sensor_sum_data = db.vesseltripdata.aggregate(
        [
            {"$match": {"tripId": trip_id, "sensorName": sensor_name}},
            {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
            {
                "$group": {
                    "_id": "$sensorName",
                    "index0_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 0]}},
                    "index1_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 1]}},
                    "index2_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 2]}},
                }
            },
        ]
    )
    # print(sensor_sum_data)
    # print(type(sensor_sum_data))
    r = list(sensor_sum_data)
    if request.GET.get("export", None) == "True":
        z = some_view(r)
        return z
    # print(dumps(list(sensor_sum_data)))
    # return HttpResponse("mani")
    return render(request, "sensor_data_avg.html", {"k": r})


# get_sensor_data_avg( sensor_name,trip_id)
def boatsensor_data_avg(request):
    trip_id = "63d4228e01afc1d6b6813e38"
    from_time = datetime.now() - timedelta(days=90)
    to_time = datetime.now()
    sensor_name = "GPS"
    # start_date=datetime.now()-timedelta(days=30)
    # end_date=datetime.now()
    boatsensor_sum_data = db.vesseltripdata.aggregate(
        [
            {
                "$match": {
                    "dateTime": {"$gte": from_time, "$lte": to_time},
                    "sensorName": sensor_name,
                }
            },
            {"$addFields": {"arraySize": {"$size": "$dataPoints"}}},
            {
                "$group": {
                    "_id": {
                        "day": {"$dayOfMonth": "$dateTime"},
                        "month": {"$month": "$dateTime"},
                        "year": {"$year": "$dateTime"},
                    },
                    "index0_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 0]}},
                    "index1_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 1]}},
                    "index2_avg": {"$avg": {"$arrayElemAt": ["$dataPoints", 2]}},
                }
            },
        ]
    )
    # print(boatsensor_sum_data)
    de = list(boatsensor_sum_data)
    if request.GET.get("export", None) == "True":
        r = some_view(de)
        return r
    # print(de)
    # print(type(boatsensor_sum_data))
    # print(dumps(list(boatsensor_sum_data)))
    # return HttpResponse("Amani")
    return render(request, "boatsensor_data.html", {"A": de})


def trip_sensors(request):
    trip_id = "63d4228e01afc1d6b6813e38"
    trip_sensors_data = db.vesseltripdata.aggregate(
        [
            {"$match": {"tripId": trip_id}},
            {"$group": {"_id": "$tripId", "sensors": {"$addToSet": "$sensorName"}}},
        ]
    )
    # print(trip_sensors_data)
    f = list(trip_sensors_data)
    print(f)
    if request.GET.get("export", None) == "True":
        r = some_view(f)
        return r
    # return HttpResponse("Anil")
    return render(request, "trip_sensors.html", {"trip": f})
    # print(type(trip_sensors_data))
    # print(dumps(list(trip_sensors_data)))


# csv function
def some_view(d):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )
    names = d[0].keys()
    writer = csv.DictWriter(response, names)
    writer.writeheader()
    writer.writerows(d)
    # writer = csv.writer(response)
    # for row in d:
    #     writer.writer(row)

    # writer.writerow(['First row', 'sensorName','dataPoints','dateTime','tripId'])
    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response


# Open File in Write mode , if not found it will create one
# File = open('test.csv', 'w+')
# d = csv.writer(File)

# # My Header
# d.writerow(('Column1', 'Column2', 'Column3'))

# # Write data
# for i in range(20):
#     d.writerow((i, i+1, i+2))

# # close my file
# File.close()
