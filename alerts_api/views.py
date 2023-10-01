from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from common.json import ModelEncoder
from .models import Alert


class AlertEncoder(ModelEncoder):
    model = Alert
    properties = [
        "alert_id",
        "model",
        "alert_type",
        "alert_ts",
        "severity",
        "team_slack",
    ]


@require_http_methods(["GET", "POST"])
def read_write_alerts(request):
    # GET Method. Read Alert based on query parameters.
    if request.method == "GET":
        serv_id = request.GET.get("service_id")
        start_ts = request.GET.get("start_ts")
        end_ts = request.GET.get("end_ts")

        if serv_id:
            try:
                query_set_with_id = Alert.objects.filter(service_id=serv_id)
                if len(query_set_with_id) != 0:
                    alerts = Alert.objects.filter(
                        service_id=serv_id, alert_ts__range=[start_ts, end_ts]
                    )
                    service_name = alerts[0].service_name
                    return JsonResponse(
                        {
                            "service_id": serv_id,
                            "service_name": service_name,
                            "alerts": alerts,
                        },
                        encoder=AlertEncoder,
                    )
                else:
                    response = JsonResponse(
                        {
                            "success": False,
                            "alert_id": "",
                            "error": "Invalid Service Id: '"
                            + serv_id
                            + "': No alerts with provided service ID exist.",
                        }
                    )
                    response.status_code = 404
                    return response
            except IndexError as e:
                response = JsonResponse(
                    {
                        "success": False,
                        "alert_id": Alert.objects.filter(service_id=serv_id)[
                            0
                        ].alert_id,
                        "error": "IndexError: "
                        + str(e)
                        + " : No alerts in timestamp range provided or timestamp.",
                    }
                )
                response.status_code = 404
                return response
            except Exception as e:
                response = JsonResponse(
                    {
                        "success": False,
                        "alert_id": Alert.objects.filter(service_id=s_id)[0].alert_id,
                        "error": str(e),
                    }
                )
                response.status_code = 500
                return response
        else:
            response = JsonResponse(
                {
                    "success": False,
                    "alert_id": "",
                    "error": "Bad Request: Missing service_id query parameter.",
                }
            )
            response.status_code = 400
            return response

    # POST method: Write Alert
    else:
        content = json.loads(request.body)
        if len(content.keys()) == 8:
            if (len(content["alert_ts"]) == 10) and (
                content["alert_ts"].isdigit() == True
            ):
                try:
                    alert = Alert.objects.create(**content)
                    return JsonResponse({"alert_id": alert.alert_id, "error": ""})
                except Exception as e:
                    response = JsonResponse(
                        {"alert_id": content["alert_id"], "error": str(e)}
                    )
                    response.status_code = 500
                    return response
            else:
                response = JsonResponse(
                    {
                        "alert_id": content["alert_id"],
                        "error:": "Invalid Parameter Entry: 'alert_ts' field must be in Unix Epoch format (10 integer digits)",
                    }
                )
                response.status_code = 500
                return response
        else:
            if "alert_id" not in content:
                response = JsonResponse(
                    {"alert_id": "", "error:": "Missing alert_id parameter"}
                )
                response.status_code = 500
                return response
            else:
                response = JsonResponse(
                    {
                        "alert_id": content["alert_id"],
                        "error:": "Missing one of more 'Alert' parameters.",
                    }
                )
                response.status_code = 500
                return response
