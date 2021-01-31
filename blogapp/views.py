from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import blog,otp,like,comment,reply
from math import ceil
import json
from django.contrib import messages
import random
from django.contrib.auth import authenticate, login
import datetime
def index(request, num=1):
	if request.method == "POST":
		userid = request.user.id
		blogid = request.POST['blogid'][4:]
		a = like.objects.filter(userid = userid, blogid= blogid)
		if(len(a)>0):
			Like = like.objects.get(userid = userid, blogid= blogid)
			Like.delete()
			status = 'disliked'
		else:
			Like = like(blogid= blogid,userid = userid)
			Like.save()
			status = 'liked'
		likes = len(like.objects.filter(blogid = blogid))
		res = json.dumps({'likes':likes,'blogid':request.POST['blogid'],'status':status})
		return HttpResponse(res)
	print(num)
	pa = 'page'+str(num)
	allblog =  blog.objects.all()[((3*num)-3):(3*num)]
	a = []
	d= 0
	mostlike = [len(like.objects.filter(blogid=allblog[0].id)),allblog[0]]
	for item in allblog:
		b = like.objects.filter(blogid=item.id)
		if len(b)>d:
			d = len(b)
			mostlike = [d,item,{'byuser':'disliked'}]
		likes={'total':len(b),'byuser':'disliked'}
		if len(b)>0:
			c = like.objects.filter(blogid=item.id,userid=request.user.id)
			if len(c)>0:
				likes['byuser']= 'liked'
				mostlike[2]['byuser']='liked'
		a.append([item,likes])			
				
	allblog = a
	n= len(blog.objects.all())
	print(blog.objects.all())
	page =n//3 + ceil((n/3)-(n//3))
	print(page)
	param = {'allblog':allblog , 'home' : 'active', 'page' : range(1,page+1),'next':(num+1)%(page+1),'mostlike':mostlike}
	return render(request , 'index.html', param )
def contact(request):
    return render(request , 'contact.html', {'contact' :'active',})
def blogs(request):
    return HttpResponse("this is blog page")
def prectices(request):
    return HttpResponse("this is prectices page")
def about(request):
    return render(request , 'aboutus.html', {'about' :'active',})
def signup(request):
	if request.method=='POST':
		email=request.POST['email']
		username = request.POST['email']
		pass1=request.POST['password']
		fname=request.POST['first_name']
		lname=request.POST['last_name']
		data= User.objects.filter(username=email)
		if len(data)>0:
			return HttpResponse(json.dumps({'text':'email'}))
		try:
			otp1=request.POST['otp']
			print("sdadasd  ",otp1)
			verify=otp.objects.filter(email=email,OTP=otp1)
			print("length of verify :",len(verify))
			if len(verify)>0:
				user = User.objects.create_user(email,email,pass1)
				print("user created /n")
				user.first_name=fname
				user.last_name=lname
				user.save()
				print("user saved /n")
				d={'text':'account'}
				resource=json.dumps(d)
				return HttpResponse(resource)
			else:
				d={'text':'invalid'}
				resource=json.dumps(d)
				return HttpResponse(resource)
				return HttpResponse()

		except Exception as e:
			print(e)
			a=""
			for i in range(6):
				a=a+str(random.randint(0,9))
			print("aaa",a)
			Otp=otp(email=email,OTP=a)
			Otp.save()
			# send_mail(
   #  		'hootspy otp',
   #  		'Here is 	YOUR OTP IS  '+a,
 		#    'ritik10120@gmail.com',
 		#    [email],
 		#    fail_silently=False,
			# )
			print("otp",a)
			d={'text':'otp','text1':'texsd'}
			resource=json.dumps(d)
			return HttpResponse(resource) 
	return render(request,'signup.html',{})
		



	# 	myuser = User.objects.create_user(email,email,pass1)
	# 	myuser.first_name= fname
	# 	myuser.last_name= lname
	# 	myuser.save()
	# 	messages.success(request,"your shoppercart account is successfully created")
	# 	return redirect('home')
	# return render(request , 'signup.html', {'signup' :'active',})
def Login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		print("email and password is "+ email + " and "+ password)
		user = authenticate(username = email, password= password)
		if user is not None:
			login(request,user)
			return HttpResponse(json.dumps({'user':'success'}))
		else:
			return HttpResponse(json.dumps({'user':'invalid'}))
	return HttpResponse("not found")

def post(request,num=1):
	if request.method=='POST':
		postfor = request.POST['for']
		print(postfor)
		if postfor == 'comment':
			com = request.POST['comment']
			userid = request.user.id
			Comment = comment(blogid= num,userid= request.user.id,comment=com)
			Comment.save()
			date = str(datetime.date.today())
			return HttpResponse(json.dumps({'comment': com , 'date': date }))
		if postfor == 'reply':
			comreply = request.POST['reply']
			comid = request.POST['comid']
			userid = request.user.id
			print(comid)
			Reply = reply(commentid=comid,comreply=comreply,comonuserid=userid)
			Reply.save()
			date = str(datetime.date.today())
			return HttpResponse(json.dumps({'reply': comreply , 'date': date }))
		if postfor == 'getreply':
			comid = request.POST['comid'][8:]
			print(comid)
			Reply = reply.objects.filter(commentid=comid)
			res = []
			for re in Reply:
				user = User.objects.get(id=re.comonuserid)
				username = user.first_name+' '+user.last_name
				rep = {
					'comreply':re.comreply,
					'commentid':re.commentid,
					'comonuserid':re.comonuserid,
					'comdate':str(re.comdate),
					'username': username
				}
				print(username)
				res.append(rep)
			responce = json.dumps(res)
			return HttpResponse(responce)
	Blog = blog.objects.get(id=num)
	comlike = []
	com = comment.objects.filter(blogid=num)
	for c in com:
		user = User.objects.get(id=c.userid)
		Reply = reply.objects.filter(commentid = c.id)
		comlike.append([c,user.first_name+' '+user.last_name,len(Reply)])
		
	return render(request, 'post.html',{'blog':Blog ,'comment':comlike})