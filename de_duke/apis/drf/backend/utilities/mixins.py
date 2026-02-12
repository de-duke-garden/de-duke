from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget


class ImageUploaderWidgetAdminMixin:
    formfield_overrides = {models.ImageField: {"widget": ImageUploaderWidget}}
