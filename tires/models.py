from django.db import models


class TiresInfo(models.Model):

    username = models.ForeignKey("users.User", on_delete=models.CASCADE)
    trim_id = models.IntegerField()
    front_width = models.IntegerField()
    front_profile = models.IntegerField()
    front_rim = models.IntegerField()
    rear_width = models.IntegerField()
    rear_profile = models.IntegerField()
    rear_rim = models.IntegerField()

    class Meta:
        db_table = "tires_info"
