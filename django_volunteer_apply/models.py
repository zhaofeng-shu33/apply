from django.db import models

class ActivityManager(models.Model):
    description = models.TextField(max_length=800, null=True, blank=True)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Activity(models.Model):
    manager = models.ForeignKey(ActivityManager, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    date = models.DateTimeField(null=True, blank=True)    
    def __str__(self):#
        return self.name

class Choice(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=800, null=True, blank=True)
    required_number = models.PositiveSmallIntegerField(default=0)
    def left_number(self):
        return self.required_number - self.person_set.count()
    def __str__(self):
        return self.activity.name + self.name

class Person(models.Model):
    name = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=(('M','Male'),('F', 'Female')), default='M')
    choices = models.ManyToManyField(Choice, blank=True)
    def __str__(self):
        return '(%s,%s)'%(self.name, self.gender)
    
