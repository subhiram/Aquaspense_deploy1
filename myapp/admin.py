from django.contrib import admin

# Register your models here.
from .models import main_crop,expenses,worker,medicine,feed,ele_bill, export,sample,daily_feed

admin.site.register(main_crop)
admin.site.register(expenses)
admin.site.register(worker)
admin.site.register(medicine)
admin.site.register(feed)
admin.site.register(ele_bill)
admin.site.register(export)
admin.site.register(sample)
admin.site.register(daily_feed)