from django.db import models


class Link(models.Model):
    author = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    date_published = models.DateField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title
