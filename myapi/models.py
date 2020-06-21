from django.db import models
# Create your models here.

class EmployeeModel(models.Model):
    id     = models.AutoField(primary_key=True)
    employee_name   = models.CharField(max_length=200, default="")
    employee_loc    = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'employees' # name of table
        app_label = 'myapi' # name of application, this should match with the application name
