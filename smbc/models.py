from django.db import models
from .links import comic_link

scores = [(i, f'{i}/5') for i in range(1, 6)]

class Comic(models.Model):
    name = models.CharField(max_length=50)
    score = models.SmallIntegerField(choices=scores)
    hide = models.BooleanField()

    def get_absolute_url(self):
        return comic_link.format(self.name)
