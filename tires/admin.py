from django.contrib import admin

from tires.models import TiresInfo


@admin.register(TiresInfo)
class TiresInfoAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "trim_id",
        "front_width",
        "front_profile",
        "front_rim",
        "rear_width",
        "rear_profile",
        "rear_rim",
    )
