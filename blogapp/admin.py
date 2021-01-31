from django.contrib import admin
# ragister your models here
from .models import blog,comment,otp,like,reply
admin.site.register(blog)
admin.site.register(comment)
admin.site.register(like)
admin.site.register(reply)
