from django.db import models

# Create your models here.

#admin and pass word is subhi
# Create your models here.
class main_crop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    crop_name = models.CharField(max_length=150)
    crop_date = models.DateField(null=False)
    crop_notes = models.TextField(max_length=200)
    location = models.CharField(max_length=100)
    user_id = models.IntegerField()
    status = models.CharField(max_length=70)
    days = models.IntegerField(null=True)

class expenses(models.Model):
    exp_no = models.AutoField(primary_key=True)
    crop_id = models.IntegerField()
    exp_name = models.CharField(max_length=150)
    exp_cost = models.IntegerField()
    exp_date = models.DateField(null=False)
    exp_paidto = models.CharField(max_length=100)
    exp_notes = models.TextField(max_length=250)

class worker(models.Model):
    worker_no = models.AutoField(primary_key=True)
    worker_name = models.CharField(max_length=100)
    date = models.DateField(null=False)
    amount = models.IntegerField()
    worker_notes = models.TextField(max_length=200)
    crop_id = models.IntegerField()

class feed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    crop_id = models.IntegerField()
    date = models.DateField(null=False)
    shop_name = models.CharField(max_length=150)
    bill_no = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    bill_amount = models.FloatField()
    quantity = models.IntegerField()
    feed_notes = models.TextField(max_length=200)

class medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    crop_id = models.IntegerField()
    med_name = models.CharField(max_length=150)
    date = models.DateField(null=False)
    bill_no = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.FloatField()
    med_notes = models.TextField(max_length=200)

class ele_bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    crop_id = models.IntegerField()
    tranformer_type = models.CharField(max_length=50)
    billed_date = models.DateField(null=False)
    start_read = models.IntegerField()
    end_read = models.IntegerField()
    bill_amount = models.FloatField()
    bill_notes = models.TextField(max_length=200)

class export(models.Model):
    exp_id = models.AutoField(primary_key=True)
    crop_id = models.IntegerField()
    date = models.DateField(null=False)
    tank_no = models.CharField(max_length=100)
    material_weight = models.FloatField()
    count = models.FloatField()
    amount = models.FloatField()
    exp_notes = models.TextField(max_length=200)

class sample(models.Model):
    num = models.IntegerField()

class daily_feed(models.Model):
    date = models.DateField(null=False)
    tank_no= models.CharField(max_length=50)
    first = models.FloatField()
    second = models.FloatField()
    third = models.FloatField()
    fourth = models.FloatField()
    crop_id = models.IntegerField()




