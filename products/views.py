from django.shortcuts import render
from .models import Entry
import smtplib
import requests

def getEmailPassword():
	email 	 = input("Enter a valid email to send mails from:")
	password = input("Enter password:")

	return email,password

def sendmail(content,receiver_mail,email,password):
	success = False
	mail = smtplib.SMTP('smtp.gmail.com',587)
	mail.ehlo()
	mail.starttls()
	try:
		mail.login(email,password)
		mail.sendmail(email,receiver_mail,content)
		mail.close()
		success = True
	except Exception:
		mail.close()

	return success

def sendSMS(content,receiver_number):
	url = "https://www.fast2sms.com/dev/bulk"
 
	payload = "sender_id=FSTSMS&message=test"
	payload += content
	temp = "&language=english&route=p&numbers="
	payload += temp
	payload += str(receiver_number)
	headers = {
	 'authorization': "poDMwbKngfyQe3VC1ZUhA5HE2dSTJxu9cqjiLGNW7zmYvlaPtkR3pHAzrBNoQv2lgaYGmZJutjfTq6Fy",
	 'Content-Type': "application/x-www-form-urlencoded",
	 'Cache-Control': "no-cache",
	 }
	 
	response = requests.request("POST", url, data=payload, headers=headers)
	 
	#print(response.text)


def createpost(request):
	post = Entry()
	post.visitor_name   = request.POST.get('visitor_name')
	post.visitor_email  = request.POST.get('visitor_email')
	post.visitor_phone  = request.POST.get('visitor_phone')
	post.check_in_time  = request.POST.get('check_in_time')
	post.check_out_time = request.POST.get('check_out_time')
	post.host_name      = request.POST.get('host_name')
	post.host_email     = request.POST.get('host_email')
	post.host_phone     = request.POST.get('host_phone')

	post.save()

	content = '\nVisitor Details: \n'
	content += 'Name: '+str(post.visitor_name)+'\n'
	content += 'Email: '+str(post.visitor_email)+'\n'
	content += 'Phone: '+str(post.visitor_phone)+'\n'
	content += 'Checkin Time: '+str(post.check_in_time)+'\n'
	content += 'Checkout Time: '+str(post.check_out_time)+'\n'

	email,password = getEmailPassword()
	success = sendmail(content,post.host_email,email,password)
	while not success:
		what = input('TLS failed, want to provide email and password again? Y/N: ')
		if what == 'N':
			print('Mail failed')
			break
		elif what == 'Y':
			email,password = getEmailPassword()
			success = sendmail(content,post.host_email,email,password)

	sendSMS(content,post.host_phone)

	return render(request, 'index.html')  

def checkOut(request):
	#print('okay')
	return render(request,'checkout.html')

def showFinalPage(request):
	name = request.POST.get('visitor_name')
	email = request.POST.get('visitor_email')
	if Entry.objects.filter(visitor_name = name,visitor_email = email).exists():
		rows = Entry.objects.filter(visitor_name = name,visitor_email = email)
	else:
		rows = []
	#print(len(rows),'here')
	if rows:
		location = input("Enter location: ")
		sender_email,password = getEmailPassword()
		for instance in rows:
			content = '\nVisit Details: \n'
			content += 'Name: '+str(instance.visitor_name)+'\n'
			content += 'Phone: '+str(instance.visitor_phone)+'\n'
			content += 'Checkin Time: '+str(instance.check_in_time)+'\n'
			content += 'Checkout Time: '+str(instance.check_out_time)+'\n'
			content += 'Host Name: '+str(instance.host_name)+'\n'
			content += 'Location: '+location+'\n'

			success = sendmail(content,email,sender_email,password)
			while not success:
				what = input('TLS failed, want to provide email and password again? Y/N: ')
				if what == 'N':
					print('Mail failed')
					break
				elif what == 'Y':
					sender_email,password = getEmailPassword()
					success = sendmail(content,email,sender_email,password)

			instance.delete()

		return render(request,'checked_out.html')

	return render(request, 'index.html')
