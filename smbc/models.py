from django.db import models

class Page(models.Model):
    max_name_len = 50

    name = models.CharField(max_length=max_name_len)
    comic = models.ImageField()
    bonus = models.ImageField()
    prev = models.CharField(max_length=max_name_len)
    next = models.CharField(max_length=max_name_len)
    title_text = models.TextField()
