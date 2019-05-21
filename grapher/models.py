from django.db import models
from django.urls import reverse
# Create your models here.

class Inputdata(models.Model):
    temperature=models.DecimalField(max_digits=6, decimal_places=3)
    radius=models.DecimalField(max_digits=19, decimal_places=3)
    def get_absolute_url(self):
        return reverse('param-detail', kwargs={'pk': self.pk})
