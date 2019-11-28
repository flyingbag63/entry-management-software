from django.db import models

# Create your models here.

class Entry(models.Model):
	visitor_name    = models.CharField(max_length = 120) 
	visitor_email 	= models.EmailField(max_length = 254)
	visitor_phone   = models.CharField(max_length = 10)
	check_in_time   = models.TimeField()
	check_out_time  = models.TimeField()
	host_name       = models.CharField(max_length = 120) 
	host_email 		= models.EmailField(max_length = 254)
	host_phone      = models.CharField(max_length = 10)