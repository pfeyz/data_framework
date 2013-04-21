from django.db import models

# Create your models here.
class TestSuite(models.Model):
    created = models.DateTimeField()
    name = models.CharField(max_length=512)
    errors = models.IntegerField()
    tests = models.IntegerField()
    failures  = models.IntegerField()
    time = models.IntegerField()

class TestCase(models.Model):
    suite_id = models.ForeignKey(TestSuite)
    name = models.CharField(max_length=512)
    errors = models.IntegerField()
    tests = models.IntegerField()
    time = models.IntegerField()

class Failure(models.Model):
    test = models.ForeignKey(TestCase)
    failure = models.CharField(max_length=512)


