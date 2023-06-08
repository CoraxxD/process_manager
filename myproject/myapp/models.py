from django.db import models

class BlacklistedProcess(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WhitelistedProcess(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
