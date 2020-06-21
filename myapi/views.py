from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http.response import JsonResponse

#import our EmployeeModel
from myapi.models import EmployeeModel
import json

@csrf_exempt
def EmployeeView(request):
    if (request.method == 'GET'):
        #get all entries from table EmployeeModel
        objects = EmployeeModel.objects.all()

        #convert django model object to json.
        response = {"data": []}
        for entry in objects:
            response["data"].append(
                {
                    "id": entry.id,
                    "employee_name": entry.employee_name,
                    "employee_loc": entry.employee_loc
                }
            )

    elif (request.method == 'POST'):
        # convert request body to json
        json_requests = json.loads(request.body.decode("utf-8") )

        # add data to EmployeeModel table.
        created = EmployeeModel.objects.create(**json_requests)
        response = {
                "id": created.id,
                "employee_name": created.employee_name,
                "employee_loc": created.employee_loc
            }

    elif (request.method == 'PUT'):
        json_requests = json.loads(request.body.decode("utf-8"))

        # check if id is not found return missing key response directly
        if "id" not in json_requests:
            return JsonResponse({"message": "Missing key 'id'"})

        object_id = json_requests["id"]
        try:
            entry = EmployeeModel.objects.get(id=object_id)
            # if employee_name is there in json requests modify employee location in current entry
            if ("employee_name" in json_requests):
                setattr(entry, "employee_name", json_requests["employee_name"])

            # if employee_loc is there in json requests modify employee location in current entry
            if ("employee_loc" in json_requests):
                setattr(entry, "employee_loc", json_requests["employee_loc"])

            entry.save()
            response = {"message": "data modified for entry with id " + str(object_id)}
        except:
            response = {"message": "Entry with id " + str(object_id) + " not found"}


    elif (request.method == 'DELETE'):
        json_requests = json.loads(request.body.decode("utf-8"))

        # check if id is not found return missing key response directly
        if "id" not in json_requests:
            return JsonResponse({"message": "Missing key 'id'"})

        object_id = json_requests["id"]
        objects_with_id = EmployeeModel.objects.filter(id=object_id)
        if (objects_with_id.count() < 1):
            response = {"message": "Entry with id " + str(object_id) + " not found"}
        else:
            objects_with_id.delete()
            response = {"message": "Deleted entry with id " + str(object_id)}

    else:
        response = {"message": "Unknown Requests type"}
    return JsonResponse(response)
