from django.db import models
import datetime
class blog(models.Model):
    blog_title = models.CharField(max_length=50)
    blog_content = models.CharField(max_length=5000)
    blog_time = models.DateField()
    blog_share = models.IntegerField(default=0)
    blog_views = models.IntegerField(default=0)
    blog_owner = models.CharField(max_length=50)
    blog_image = models.ImageField(upload_to = 'blog/images', default= "")
class comment(models.Model):
	"""docstring for likecomment"""
	blogid = models.CharField(max_length=50,primary_key=False)
	userid = models.CharField(max_length=50,primary_key=False)
	comment = models.CharField(max_length=500)
	date = models.DateField(default=datetime.date.today)

class otp(models.Model):
	email=models.CharField(max_length=50,primary_key=True)
	OTP=models.CharField(max_length=50)
class like(models.Model):
	"""docstring for likecomment"""
	blogid = models.CharField(max_length=50,primary_key=False)
	userid = models.CharField(max_length=50,primary_key=False)
class reply(models.Model):
    comreply  = models.CharField(max_length=500)
    commentid = models.CharField(max_length=50)
    comonuserid = models.CharField(max_length=50)
    comdate = models.DateField(default=datetime.date.today)

