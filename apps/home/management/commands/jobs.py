from django.conf import settings
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from apps.home.models import Category,Case,Contact,State
from django.contrib.auth.models import User,Group
from django.contrib import messages
import random
import string
import random_word
from django.contrib.auth import authenticate, login
from django_messages.models import Message
from django.http import JsonResponse
from apps.home.mailfetch import fetch_unread_email
from django.core.mail import send_mail
from django.conf import settings



def whistleblower_user():
    random_word_str = random_word.RandomWords().get_random_word()
    random_number = random.randint(1000, 9999)
    return f"{random_word_str}{random_number}"

def schedule_api():

	print('yes')

def case_mail_add(request):
    
    # Extract data from the form
    username = whistleblower_user()
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))  # Random password
    user = User.objects.create_user(username, '', password)
    group = Group.objects.get(name='WhistleBlower')  # Get the group by name
    user.groups.add(group)  # Add the user to the group
    email_info_list = fetch_unread_email()

    try:
        new_state = State.objects.get(Name='New')
    except State.DoesNotExist:
        new_state = None

    try:
        cate = Category.objects.get(Name='Other')
    except Category.DoesNotExist:
        cate = None

    channel = 'Email'
    print(new_state)
    print(email_info_list)
    for email_info in email_info_list:
        print(user)
        Case_data = {
            'Title': email_info['subject'],
            'Description': email_info['body'],
            'Category': cate,
            'Reporting_Channel': channel,
            'State': new_state,
            'whistleblower': user,
        }

        Contact_data = {
            'eMail_address': email_info['sender'],
            'whistleblower': user,
        }

        Message_data = {
            'subject': email_info['subject'],
            'body': email_info['body'],
            'sender': user,
            'recipient': user,
        }

        # Insert data into Table1
        Case_instance = Case.objects.create(**Case_data)
        # Insert data into Table2
        Contact_instance = Contact.objects.create(**Contact_data)
            # Register a new user
        Contact_instance = Message.objects.create(**Message_data)


        sender_email = settings.DEFAULT_FROM_EMAIL
        subject = 'Case Submission Confirmation'
        message = f'Thank you for submitting your case. Your case has been received and will be reviewed promptly. Below are credentials to access your case  User Name: {username} password: {password}Copy the Credentials and use them to login and view your case http://127.0.0.1:8000/inbox/'
        from_email = sender_email  # Update with your email address
        recipient_list = [email_info['sender']]
        send_mail(subject, message, from_email, recipient_list)






        # Optionally, perform any additional logic here 
    #success_message = f'Your Case has been submitted succesfully </br>Below are credentials to access your case are below </br></br><b>User Name:</b> {username} </br> <b>password:</b> {password}</br></br>Copy the Credentials and use them to login and view your case  ' # Optional: Display a success message with the generated username and password
    return render(request, 'home/input-areas-forms.html')
