from django.db import models


class Alert(models.Model):
    alert_id = models.CharField(max_length=50, unique=True)
    service_id = models.CharField(max_length=200, null=False)
    service_name = models.CharField(max_length=200, null=False)
    model = models.CharField(max_length=100, null=False)
    alert_type = models.CharField(max_length=100, null=False)
    alert_ts = models.CharField(max_length=10, null=False)
    severity = models.CharField(max_length=100, null=False)
    team_slack = models.CharField(max_length=100, null=False)

    # order Alert objects by timestamp
    class Meta:
        ordering = ("alert_ts", "alert_id")
