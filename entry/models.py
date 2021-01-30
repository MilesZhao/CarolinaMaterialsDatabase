from django.db import models

# Create your models here.
class Spacegroup(models.Model):
    number = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=25)
    hall = models.CharField(max_length=25)
    point_group = models.CharField(max_length=25)
    crystal_system = models.CharField(max_length=25)

    class Meta:
        db_table = "spacegroups"

class Entry(models.Model): 
    file_path = models.CharField(max_length=200)
    formula = models.CharField(max_length=50)
    formation_energy = models.FloatField()
    natom = models.IntegerField()
    element_list = models.CharField(max_length=25)
    spacegroup = models.ForeignKey(Spacegroup, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date created')
    generic = models.CharField(max_length=25, default='')
    volume = models.FloatField(default=0.0)
    nelement = models.IntegerField(default=0)

    class Meta:
        db_table = "entries"
