import json
from .models import Alert
from django.test import TransactionTestCase, Client


class Tests(TransactionTestCase):
    # Testing POST Requests:
    def test_alert_create_1(self):
        client = Client()
        body = {
            "alert_id": "b950482e9911ec7e41f7ca5e5d9a424f",
            "service_id": "my_test_service_id",
            "service_name": "my_test_service",
            "model": "my_test_model",
            "alert_type": "anomaly",
            "alert_ts": "1695644160",
            "severity": "warning",
            "team_slack": "slack_ch",
        }
        response = client.post(
            "/api/alerts/", json.dumps(body), content_type="application/json"
        )

        self.assertEqual(
            response.status_code, 200, msg="Did not get a 200 OK for /alerts"
        )

    # missing alert_id catch
    def test_alert_create_2(self):
        client = Client()
        body = {
            "service_id": "my_test_service_id",
            "service_name": "my_test_service",
            "model": "my_test_model",
            "alert_type": "anomaly",
            "alert_ts": "1695644160",
            "severity": "warning",
            "team_slack": "slack_ch",
        }
        response = client.post(
            "/api/alerts/", json.dumps(body), content_type="application/json"
        )

        self.assertEqual(response.status_code, 500, msg="Did not get a 500 for /alerts")

    # invalid timestamp format handling test
    def test_alert_create_3(self):
        client = Client()
        body = {
            "alert_id": "b950482e9911ec7e41f7ca5e5d9a424f",
            "service_id": "my_test_service_id",
            "service_name": "my_test_service",
            "model": "my_test_model",
            "alert_type": "anomaly",
            "alert_ts": "169564416h",
            "severity": "warning",
            "team_slack": "slack_ch",
        }
        response = client.post(
            "/api/alerts/", json.dumps(body), content_type="application/json"
        )

        self.assertEqual(response.status_code, 500, msg="Did not get a 500 for /alerts")

    # missing one or more parameters
    def test_alert_create_4(self):
        client = Client()
        body = {
            "alert_id": "b950482e9911ec7e41f7ca5e5d9a424f",
            "service_id": "my_test_service_id",
            "service_name": "my_test_service",
            "model": "my_test_model",
        }
        response = client.post(
            "/api/alerts/", json.dumps(body), content_type="application/json"
        )

        self.assertEqual(response.status_code, 500, msg="Did not get a 500 for /alerts")

    # Testing GET alert with queries:
    def test_alert_read_1(self):
        Alert.objects.create(
            alert_id="b950482e9911ec7e41f7ca5e5d9a424f",
            service_id="my_test_service_id",
            service_name="my_test_service",
            model="my_test_model",
            alert_type="anomaly",
            alert_ts="1696196004",
            severity="warning",
            team_slack="slack_ch",
        )
        Alert.objects.create(
            alert_id="b950482e9911ec7e413fca5e5d9a424f",
            service_id="my_test_service_id",
            service_name="my_test_service",
            model="my_test_model",
            alert_type="anomaly",
            alert_ts="1696282404",
            severity="warning",
            team_slack="slack_ch",
        )

        client = Client()
        response = client.get(
            "/api/alerts/",
            {
                "service_id": "my_test_service_id",
                "start_ts": "1696109604",
                "end_ts": "1696368804",
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code, 200, msg="Did not get a 200 OK for /alerts"
        )
        self.assertEqual(
            len(data["alerts"]),
            2,
            msg="Did not correct number of alerts in time range (2).",
        )

    # Invalid Service Id
    def test_alert_read_2(self):
        Alert.objects.create(
            alert_id="b950482e9911ec7e41f7ca5e5d9a424f",
            service_id="my_test_service_id",
            service_name="my_test_service",
            model="my_test_model",
            alert_type="anomaly",
            alert_ts="1695644160",
            severity="warning",
            team_slack="slack_ch",
        )
        client = Client()
        response = client.get("/api/alerts/", {"service_id": "my_test_service_test"})

        self.assertEqual(response.status_code, 404, msg="Did not get a 404 for /alerts")

    # Missing Service Id
    def test_alert_read_3(self):
        client = Client()
        response = client.get("/api/alerts/")

        self.assertEqual(response.status_code, 400, msg="Did not get a 400 for /alerts")

    # Invalid Timestamp Range
    def test_alert_read_4(self):
        Alert.objects.create(
            alert_id="b950482e9911ec7e41f7ca5e5d9a424f",
            service_id="my_test_service_id",
            service_name="my_test_service",
            model="my_test_model",
            alert_type="anomaly",
            alert_ts="1696196004",
            severity="warning",
            team_slack="slack_ch",
        )
        Alert.objects.create(
            alert_id="b950482e9911ec7e413fca5e5d9a424f",
            service_id="my_test_service_id",
            service_name="my_test_service",
            model="my_test_model",
            alert_type="anomaly",
            alert_ts="1696282404",
            severity="warning",
            team_slack="slack_ch",
        )

        client = Client()
        response = client.get(
            "/api/alerts/",
            {
                "service_id": "my_test_service_id",
                "start_ts": "0000000000",
                "end_ts": "0000000000",
            },
        )

        self.assertEqual(response.status_code, 404, msg="Did not get a 404 for /alerts")
