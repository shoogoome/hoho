from django.db import models


class PhotoModel(models.Model):

    class Meta:
        verbose_name = "照片表"
        verbose_name_plural = "照片表"

    # 照片归属
    association = models.ForeignKey('association.Association', null=True, blank=True, on_delete=models.SET_NULL)

    # 照片地址
    photo_path = models.CharField(max_length=200, default='', blank=True)


    def __str__(self):
        return "[归属] %s [地址] %s" % (str(self.association.name), self.photo_path)
