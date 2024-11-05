import imaplib
import email
import random
import string
import random_word
import re
from django.http import HttpRequest

from django.http import HttpResponse
from apps.home.forms import CaseContactForm
from apps.home.models import Message, Case, Contact
from django.contrib.auth.models import User, Group
from django.shortcuts import render

def extract_email_address(sender):
    match = re.search(r'[\w\.-]+@[\w\.-]+', sender)
    return match.group() if match else None

def fetch_unread_email(imap_server, username, password, mailbox='inbox'):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select(mailbox)

    status, messages = mail.search(None, 'UNSEEN')
    email_info_list = []

    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg['subject']
        sender = extract_email_address(msg['from'])
        date = msg['date']

        if msg.is_multipart():
            text = ''.join(part.get_payload() for part in msg.get_payload() if part.get_content_type() == 'text/plain')
        else:
            text = msg.get_payload()

        email_info = {
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': text
        }

        email_info_list.append(email_info)

    mail.close()
    mail.logout()

    return email_info_list

def whistleblower_user():
    random_word_str = random_word.RandomWords().get_random_word()
    random_number = random.randint(1000, 9999)
    return f"{random_word_str}{random_number}"

def case_email11_add(request):
    imap_server = 'mail.computaq.co.zm'
    username = 'blower@computaq.co.zm'
    password = 'Mik-dy2021'

    email_info_list = fetch_unread_email(imap_server, username, password)
    
    form = CaseContactForm(request.POST)

    if form.is_valid():
        username = whistleblower_user()
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        user = User.objects.create_user(username, '', password)
        group = Group.objects.get(name='WhistleBlower')
        user.groups.add(group)

        for email_info in email_info_list:
            Case_data = {
                'Title': email_info['subject'],
                'Description': email_info['body'],
                'Category': form.cleaned_data['Category'],
                'Privacy': form.cleaned_data['Privacy'],
                'State': form.cleaned_data['State'],
                'Closing_code': form.cleaned_data['Closing_code'],
                'whistleblower': user,
            }

            Contact_data = {
                'Name': form.cleaned_data['Name'],
                'Phone_Number': form.cleaned_data['Phone_Number'],
                'eMail_address': form.cleaned_data['eMail_address'],
                'Address_1': form.cleaned_data['Address_1'],
                'Address_2': form.cleaned_data['Address_2'],
                'whistleblower': user,
            }

            Message_data = {
                'subject': email_info['subject'],
                'body': email_info['body'],
                'sender': user,
                'recipient': user,
            }

            Case_instance = Case.objects.create(**Case_data)
            Contact_instance = Contact.objects.create(**Contact_data)
            Message_instance = Message.objects.create(**Message_data)

        success_message = f'Your Case has been submitted successfully. Below are credentials to access your case: <br><b>User Name:</b> {username}<br><b>Password:</b> {password}<br><br>Copy the credentials and use them to login and view your case.'

        return render(request, 'home/input-areas-forms.html', {'success_message': success_message})
    
    # Return the form in the context if it's not valid
    return render(request, 'home/input-areas-forms.html', {'form': form})
