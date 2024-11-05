# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.db.models import Sum
import time
from django.db.utils import OperationalError
import json
from django.shortcuts import redirect, render,get_object_or_404
from .models import *
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import random_word
from .forms import *
from django.views.generic.edit import FormView
from django.views.generic import ListView, CreateView,DetailView,UpdateView 
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction as db_transaction
from django.contrib.staticfiles.storage import staticfiles_storage
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OuterRef, Subquery

def send_account_info(request):
    # Example data, replace with actual data from your form or model
    username = 'example_user'
    password = 'example_password'
    email = 'elly@computaq.co.zm'
    
    send_mail(
        'Your Account Information',
        f'Username: {username}\nPassword: {password}',
        settings.DEFAULT_FROM_EMAIL,  # or 'lifeplus@computaq.co.zm'
        [email],
        fail_silently=False,
    )

    return HttpResponse('Email sent successfully!')


current_date = timezone.now()
end_of_month = (current_date + relativedelta(day=31)).date()
end_of_week = (current_date + relativedelta(day=7)).date()




def random_works():
    r = random_word.RandomWords()
    random_word_str = r.get_random_word()  # Get a random word
    if len(random_word_str) < 8:
        # If the word is shorter than 8 characters, pad it with random letters
        random_word_str = random_word_str.ljust(8, random.choice(string.ascii_lowercase))
    elif len(random_word_str) > 8:
        # If the word is longer than 8 characters, truncate it to 8 characters
        random_word_str = random_word_str[:8]
    
    random_number = random.randint(1000, 9999)
    return f"{random_word_str}{random_number}"


#@login_required(login_url="/login/")

def test(request):
    context = {}
    html_template = loader.get_template('home/html/elements-dropdowns.html')
    return HttpResponse(html_template.render(context,request))


def test1(request):
    context = {}
    html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render(context,request))

def index(request):
    products = Products.objects.all().values(),
    context = {
        'products': products
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context,request))

class Dashboard(ListView):
    model = Products  # Correct attribute name
    template_name = 'home/dashboard.html'   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Orders.objects.all().values()
        bonus = Transaction_Bonus.objects.filter(status='Pending')
        # Add any extra context you need here

        context['order'] = order
        return context
    
class DashboardOrder(ListView):
    model = Products  # Correct attribute name
    template_name = 'home/orderpage.html'   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # First, get the latest order date for each user that matches the package name
        package_id = 1  # or any other package ID you want to filter by
        orders_product_1 = Orders.objects.filter(
            user=OuterRef('user'),
            package_id=package_id
        ).order_by('-order_date')

        orders_product_2 = Orders.objects.filter(
            user=OuterRef('user'),
            package_id=2
        ).order_by('-order_date')
        
        # Add any extra context you need here
        latest_orders = Orders.objects.filter(user=OuterRef('user')).order_by('-order_date')
        latest_orders_per_user = Orders.objects.filter(
            order_date=Subquery(latest_orders.values('order_date')[:1])
        ).values(
            'user__first_name', 
            'user__last_name', 
            'order_date', 
            'package__package_name', 
            'package__package_price'
        )
        order = latest_orders_per_user.distinct()

        context['order_data'] = order
        return context


class DashboardBonus(ListView):
    model = Products  # Correct attribute name
    template_name = 'home/bonuspage.html'   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Orders.objects.all().values()
        bonus = Transaction_Bonus.objects.filter().values('user__username','user__first_name','user__last_name','status', 'tran_code__tran_bonus__bonus','rundate','trandate','id')
        # Add any extra context you need here
        getbonus = Product_bonus.objects.filter(flag = True ).values()
        context['bonus_data'] = bonus
        context['getbonus_data'] = getbonus
        return context


class DashboardTransactions(FormView):
    model = Products  # Correct attribute name
    template_name = 'home/Trasnactionpage.html'
    form_class = TransferToAccountForm
    
    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs,)
        adminuser = self.request.user
        source_account_type = AccType.objects.get(id=1),
        if request.method == 'POST':
            if 'search_destination' in request.POST:
                form = TransferToAccountForm(request.POST)
                if form.is_valid():
                    destination_user = form.cleaned_data['destination_user']
                    try:
                        searched_user = MyUser.objects.get(username=destination_user)
                    except MyUser.DoesNotExist:
                        messages.error(request, f'User with username "{destination_user}" does not exist.')
       
        context['form'] = self.get_form()
        context['form'].fields['source_user'].initial = adminuser 
        context['form'].fields['destination_acc_type'].initial = source_account_type
        
        account = Account.objects.filter(acc_type=4, acc_holder=adminuser).values('cur_bal')
        bonus = Transaction_Bonus.objects.filter().values('user__username','user__first_name','user__last_name','status', 'tran_code__tran_bonus__bonus','rundate','trandate','id')
        transaction = Transaction.objects.filter(accType=4, user=adminuser).values()
        # Add any extra context you need here
        getbonus = Product_bonus.objects.filter(flag = True ).values()
        context['bonus_data'] = bonus
        context['getbonus_data'] = getbonus
        context['account_data'] = account
        context['transaction_data'] = transaction
        #context['form'] = TransferToAccountForm()
        return context
    
    def form_valid(self, form):
        user = get_object_or_404(MyUser, pk=self.request.user.pk)
        destination_user = form.cleaned_data['destination_user']
        source_acc_type = form.cleaned_data['source_acc_type']
        destination_acc_type = form.cleaned_data['destination_acc_type']
        amount = form.cleaned_data['amount']
        retries = 3
        for attempt in range(retries):
            try:
                with db_transaction.atomic():

                    source_account = Account.objects.get(acc_holder=user, acc_type=source_acc_type)
                    destination_account = Account.objects.get(acc_holder=user, acc_type=destination_acc_type)
                    print(source_account)
                    if source_account.cur_bal < amount:
                        raise ValueError("Insufficient balance.")

                    Transaction.objects.create(
                        accType=AccType.objects.get(id=source_acc_type.id),
                        user=user,
                        amount=-amount,
                        desc = 'E-Transfer',
                        tran_code=Transaction_codes.objects.get(tran_code=350)
                    )

                    Transaction.objects.create(
                        accType=AccType.objects.get(id=destination_acc_type.id),
                        user=destination_user,
                        amount=amount,
                        tran_code=Transaction_codes.objects.get(tran_code=100)
                    )

                return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})
            except OperationalError:
                if attempt < retries - 1:
                    time.sleep(1)  # Wait before retrying
                else:
                    raise  # Reraise the exception if max retries are exceeded

        # This line should not be reached
        raise Exception("Failed to complete the transaction after multiple attempts.")

    def get_success_url(self):
        return reverse('apps_home:DashboardTransactions')


"""class DashboardTransactions(FormView):
    model = Products
    template_name = 'home/Transactionpage.html'
    form_class = TransferToAccountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form'] = form  # Add the form to the context
        user = get_object_or_404(MyUser, pk=self.request.user.pk)
        adminuser = self.request.user

        # Collect account, bonus, and transaction data
        context['account_data'] = Account.objects.filter(acc_type=4, acc_holder=adminuser).values('cur_bal')
        context['bonus_data'] = Transaction_Bonus.objects.all().values('user__username', 'user__first_name', 
                                                                    'user__last_name', 'status', 
                                                                    'tran_code__tran_bonus__bonus', 
                                                                    'rundate', 'trandate', 'id')
        context['transaction_data'] = Transaction.objects.filter(accType=4, user=adminuser).values()
        context['getbonus_data'] = Product_bonus.objects.filter(flag=True).values()
        context['form'].fields['source_user'].initial = adminuser
        context['form'].fields['source_user'].initial = adminuser

        # Handle form submission for searching users and making transfers
        if self.request.method == 'POST':
            if 'search_destination' in self.request.POST:
                searched_user = self.handle_user_search(context, form)
                if searched_user:
                    # Set the initial value for destination_user to the searched user
                    
                    if searched_user:
                        # Pass the queryset for the destination_user
                        context['form'] = TransferToAccountForm(destination_user_queryset=MyUser.objects.filter(pk=searched_user.pk))
                       
            if 'make_transfer' in self.request.POST:
                self.handle_transfer(context, form, user, adminuser)

        context['formSearch'] = selectAccountForm()
        return context

    def handle_user_search(self, context, form):
        formSearch = selectAccountForm(self.request.POST)
        if formSearch.is_valid():
            destination_user = formSearch.cleaned_data['usercode']
            try:
                searched_user = MyUser.objects.get(usercode=destination_user)
                messages.success(self.request, f'User "{searched_user.username}" found.')
                
                return searched_user  # Return the found user
            except MyUser.DoesNotExist:
                messages.error(self.request, f'User with username "{destination_user}" does not exist.')
        return None
    def handle_transfer(self, context, form, user, adminuser):
        source_acc_type = form.cleaned_data['source_acc_type']
        destination_user = form.cleaned_data['destination_user']
        amount = form.cleaned_data['amount']
        retries = 3

        for attempt in range(retries):
            try:
                with db_transaction.atomic():
                    source_account = Account.objects.get(acc_holder=user, acc_type=source_acc_type)
                    destination_account = Account.objects.get(acc_holder=destination_user, acc_type=form.cleaned_data['destination_user'])

                    if source_account.cur_bal < amount:
                        raise ValueError("Insufficient balance.")

                    # Create transaction records
                    Transaction.objects.create(
                        accType=AccType.objects.get(id=source_acc_type.id),
                        user=user,
                        amount=-amount,
                        desc='E-Transfer',
                        tran_code=Transaction_codes.objects.get(tran_code=350)
                    )
                    print()
                    Transaction.objects.create(
                        accType=AccType.objects.get(id=form.cleaned_data['destination_user'].id),
                        user=destination_user,
                        amount=amount,
                        tran_code=Transaction_codes.objects.get(tran_code=100)
                    )

                return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})

            except OperationalError:
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    messages.error(self.request, "Transaction failed due to a database error.")
                    break
            except Exception as e:
                messages.error(self.request, str(e))
                break

    def get_success_url(self):
        return reverse('apps_home:DashboardTransactions')"""



def post_weekend_transaction(request, **kwargs):
    print("Request Method:", request.method)  # Debug line
    print("POST Data:", request.POST)  
    if request.method == 'POST':
        if 'weekend_process' in request.POST:
            
            pending_bonuses = Transaction_Bonus.objects.filter(status='Pending', tran_code=500)
            
            if pending_bonuses.exists():
                for bonus in pending_bonuses:
                    user_instance = get_object_or_404(MyUser, pk=bonus.user_id)
                    # Create the Transaction object for each bonus
                    Transaction.objects.create(
                        accType=bonus.accType,
                        user=user_instance,
                        tran_code=bonus.tran_code,
                        desc=bonus.desc,
                        product=bonus.product,
                        amount=bonus.amount
                    )
                # Update the status of all Transaction_Bonus to 'Processed'
                pending_bonuses.update(status='Processed')

                return HttpResponse("All pending transactions processed successfully.")
            else:
                return HttpResponse("No pending transactions to process.")
    return HttpResponse("Invalid request method or missing 'weekend_process' key.")


def post_transaction(request, **kwargs):
    if request.method == 'POST':
        if 'process' in request.POST:
            # Retrieve all Transaction_Bonus objects with status 'Pending'
            pending_bonuses = Transaction_Bonus.objects.filter(status='Pending', tran_code=300)

            if pending_bonuses.exists():
                # Aggregate amounts by user
                user_amounts = pending_bonuses.values('user').annotate(total_amount=Sum('amount'))

                for user_amount in user_amounts:
                    user_id = user_amount['user']
                    total_amount = user_amount['total_amount']

                    # Retrieve the MyUser instance
                    user_instance = get_object_or_404(MyUser, pk=user_id)

                    # Get the parents of the user
                    user_hierarchy = BonusPay.matching_bonus_hierarchies(user_instance.username)
                    userParent = user_hierarchy[user_instance.username][:5]  # Get top 5 parents
                    # Calculate share for each parent
                    parent_count = len(userParent)
                    if parent_count > 0:
                        share_amount = total_amount / parent_count

                        for parent in userParent:
                            parent_user_instance = get_object_or_404(MyUser, pk=parent.id)  # Assuming parent.id is the user ID
                            # Create a Transaction object for each parent
                            Transaction.objects.create(
                                accType=pending_bonuses.filter(user=user_instance).first().accType,
                                user=parent_user_instance,
                                tran_code=pending_bonuses.filter(user=user_instance).first().tran_code,
                                desc=pending_bonuses.filter(user=user_instance).first().desc,
                                product=pending_bonuses.filter(user=user_instance).first().product,
                                amount=share_amount
                            )

                    # Update the status of all Transaction_Bonus for this user
                    pending_bonuses.filter(user=user_instance).update(status='Processed')

                return HttpResponse("All pending transactions processed and amounts distributed to parents successfully.")
            else:
                return HttpResponse("No pending transactions to process.")
    return HttpResponse("Invalid request method or missing 'process' key.")




    
    
                
            


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    



class UserNode:
    def __init__(self, user, relationship=None):
        self.user = user
        self.relationship = relationship  # Indicates the relationship ('parent', 'child', 'grandchild', ...)
        self.children = []
        self.order= Orders.objects.filter(user=user).last()
       

    def add_child(self, child, relationship=None):
        child_node = UserNode(child, relationship)
        self.children.append(child_node)

    def count_children(self):
        """Returns the number of direct children for this node."""
        return len(self.children)
    
    def count_total_descendants(self):
        """Returns the total number of all descendants (children, grandchildren, etc.) for this node."""
        total = len(self.children)  # Start with direct children count
        for child in self.children:
            total += child.count_total_descendants()  # Recursively add each child's descendants
        return total

    def show_hierarchy(self, depth=0, max_depth=10):
        hierarchy = {
            'user': self.user.username,
            'status': self.user.my_status,
            'relationship': self.relationship if self.relationship else 'parent',
            'order': self.order.package if self.order else 'No order',
            'orderPrice': self.order.package.package_price if self.order else 'No order',
            'numberOfChildren': self.count_children(),
            'totalDescendants': self.count_total_descendants(),
            'children': [],
        }

        if depth < max_depth:
            for child in self.children:
                hierarchy['children'].append(child.show_hierarchy(depth + 1, max_depth))

        return hierarchy

def fetch_and_add_children(node, max_depth):
    if max_depth > 0:
        children = MyUser.objects.filter(parent=node.user)
        for child in children:
            node.add_child(child, relationship='child')
            fetch_and_add_children(node.children[-1], max_depth - 1)

def generate_html_from_hierarchy(hierarchy):
    image_url = staticfiles_storage.url('assets/img/user.png')
    html = f'''
    <li class="member-item">
        <a href="javascript:void(0);">
            <div class="member-view-box">
                <div class="member-image">
                    <img src="{image_url}" alt="Member">
                    <div class="member-details">
                        <h5>{hierarchy['user']}</h5>
                        <p>{hierarchy['order']}</p>
                        <p>{hierarchy['status']}</p>
                        <!--<p>{hierarchy['orderPrice']}</p>-->
                        <p>{hierarchy['numberOfChildren']}</p>
                        <p>{hierarchy['totalDescendants']}</p>
                        
                        
                    </div>
                </div>
            </div>
        </a>
        <ul class="member-children">
    '''

    for child in hierarchy['children']:
        html += generate_html_from_hierarchy(child)

    html += '</ul></li>'
    return html


@login_required(login_url="/login/")
def genealogy_view(request):
    root_user = request.user
    root_user = MyUser.objects.filter(parent__isnull=True).first()  # Assuming the root user has no parent
    if root_user:
        root_node = UserNode(user=root_user, relationship='root')
        fetch_and_add_children(root_node, max_depth=3)
        hierarchy_data = root_node.show_hierarchy()
        html_output = generate_html_from_hierarchy(hierarchy_data)
    else:
        html_output = '<li>No data available</li>'

    return render(request, 'home/genealogy.html', {'html_output': html_output})




# Assuming `start_user` is an instance of `MyUser`: direct matching bunus
class BonusPay(ListView):
    model = MyUser
    template_name = 'home/billing.html'

    @staticmethod
    def get_all_users():
        users = MyUser.objects.all()
        return list(users)

    @staticmethod
    def build_user_hierarchy(users_list, max_depth=3):
        hierarchies = {}
        for user in users_list:
            root_node = UserNode(user)
            fetch_and_add_children(root_node, max_depth)
            hierarchies[user.username] = root_node.show_hierarchy()
        return hierarchies

    #process_and_hierarchies
    @classmethod
    def create_transactions_for_user(cls, user_instance, hierarchy, depth=0, total_descendants=None):
        acctype = AccType.objects.get(id=2)
        tran_code = Transaction_codes.objects.get(tran_code=300)
        tran_code_per = tran_code.tran_bonus.percentage
        # Transaction details
        productPrice = Decimal(hierarchy['orderPrice']) if hierarchy['orderPrice'] != 'No order' else Decimal('0')
        
        if total_descendants is None:
            # Set the total descendants from the root user's hierarchy
            total_descendants = Decimal(hierarchy['totalDescendants'])

        # Create a transaction based on the total number of descendants
        if total_descendants >= 0:
            for child in hierarchy['children']:
                child_user = MyUser.objects.get(username=child['user'])
                per = Decimal(tran_code_per) / Decimal('100')
                amount = (productPrice * per) / total_descendants
                # Only create a transaction for non-root users
                if depth > 0:
                    desc = (f'Bonus from - {child_user.username} - '
                            f'{Transaction_codes.objects.get(tran_code=300).tran_bonus.bonus}')

                    Transaction.objects.create(
                        accType=acctype,
                        order_date=timezone.now(),
                        user=user_instance,
                        tran_code=tran_code,
                        desc=desc,
                        amount=amount
                    )
                # Recur for the child's children
                cls.create_transactions_for_user(user_instance, child, depth + 1, total_descendants)

    @classmethod
    def points_hierarchies(cls, user, max_depth=1, product_instance=None):
        users = cls.get_all_users()
        user_hierarchies = cls.build_user_hierarchy(users, max_depth)
        all_parents_hierarchies = {}

        try:
            # Get the user instance from the specified username
            user_instance = MyUser.objects.get(username=user)
            # Get parents from bottom to root
            parents = cls.get_parents_bottom_to_root(user_instance)
            # Store the parent details only for the specified user
            all_parents_hierarchies[user] = parents
            userParent = all_parents_hierarchies[user][:5]
            # Call post_points with the user instance and hierarchy details
            cls.post_points(user_instance, userParent, product_instance, parents)
            
        except MyUser.DoesNotExist:
            print(f"User '{user}' does not exist.")

        return all_parents_hierarchies

    @classmethod
    def post_points(cls, user, userParent, product_instance, hierarchy, depth=0, total_descendants=None):
        # Transaction details
        total_descendants = 4
        
        # Create a transaction based on the total number of descendants
        if total_descendants >= 0:
            # Points amount to be given to the parent
            points = product_instance.points
            for userParent in userParent:
            # Recur for the child's children first (post points bottom-up)
                print(userParent, points)

                if userParent:
                    points_entry, created = PointsModel.objects.get_or_create(
                        member=userParent,
                        #product=product_instance,
                        defaults={'points': points}  # Set initial points if creating
                    )
                    if not created:
                        # If it already existed, update the points
                        points_entry.points += points
                        points_entry.save()


    @classmethod
    def get_parents_bottom_to_root(cls, user_instance):
        parents = []
        while user_instance.parent:
            parents.append(user_instance.parent)
            user_instance = user_instance.parent
        return parents


    




    @classmethod
    def print_all_user_hierarchies(cls, max_depth=3):
        users = cls.get_all_users()
        user_hierarchies = cls.build_user_hierarchy(users, max_depth)
        
        for username, hierarchy in user_hierarchies.items():
            try:
                # Get the user instance from the username
                user_instance = MyUser.objects.get(username=username)

                # Create transactions for the hierarchy associated with the user
                cls.create_transactions_for_user(user_instance, hierarchy)

            except MyUser.DoesNotExist:
                print(f"User with username {username} does not exist.")

    



    ##weekend bonus
    @classmethod
    def create_transactions_for_user(cls, user_instance, hierarchy, depth=0, total_descendants=None):
        acctype = AccType.objects.get(id=2)
        tran_code = Transaction_codes.objects.get(tran_code=500)
        tran_code_per = tran_code.tran_bonus.percentage

        # Transaction details
        productPrice = Decimal(hierarchy['orderPrice']) if hierarchy['orderPrice'] != 'No order' else Decimal('0')
        
        if total_descendants is None:
            # Set the total descendants from the root user's hierarchy
            total_descendants = Decimal(hierarchy['totalDescendants'])

        # Create a transaction based on the total number of descendants
        if total_descendants >= 0:
            for child in hierarchy['children']:
                child_user = MyUser.objects.get(username=child['user'])
                per = Decimal(tran_code_per) / Decimal('100')
                amount = (productPrice * per) / total_descendants
             
                # Only create a transaction for non-root users
                if depth > 0:
                    desc = (f'Bonus from - {child_user.username} - '
                            f'{Transaction_codes.objects.get(tran_code=500).tran_bonus.bonus}')

                    Transaction.objects.create(
                        accType=acctype,
                        order_date=timezone.now(),
                        user=user_instance,
                        tran_code=tran_code,
                        desc=desc,
                        amount=amount
                    )
                # Recur for the child's children
                cls.create_transactions_for_user(user_instance, child, depth + 1, total_descendants)

    @classmethod
    def create_weekend_bonus(cls, user, userParent, product_instance, hierarchy, depth=0, total_descendants=None):
        acctype = AccType.objects.get(id=2)
        tran_code = Transaction_codes.objects.get(tran_code=500)
        tran_code_per = tran_code.tran_bonus.percentage
        total_descendants = 4
        
        # Transaction details
        
        
        productPrice = product_instance.package_price
        
        """if total_descendants is None:
            # Set the total descendants from the root user's hierarchy
            total_descendants = Decimal(hierarchy['totalDescendants'])"""

        # Create a transaction based on the total number of descendants
        if total_descendants >= 0:
            #for child in hierarchy['children']:
            for userParent in userParent:
                #child_user = MyUser.objects.get(username=child['user'])
                if userParent:
                    
                    per = Decimal(tran_code_per) / Decimal('100')
                    amount = (productPrice * per) / total_descendants
                   
                    # Only create a transaction for non-root users
                    
                    desc = (f'Bonus from -  - '
                            f'{Transaction_codes.objects.get(tran_code=500).tran_bonus.bonus}')
                   
                    Transaction_Bonus.objects.create(
                        rundate=end_of_week,
                        accType=acctype,
                        user=userParent,
                        tran_code=tran_code,
                        desc=desc,
                        amount=amount
                        
                    )
                    print(userParent, amount)
                # Recur for the child's children
                #cls.create_weekend_bonus(user_instance, child, depth + 0, total_descendants)

    @classmethod
    def weekend_all_user_hierarchies(cls, user, max_depth=1, product_instance=None):
        users = cls.get_all_users()
        user_hierarchies = cls.build_user_hierarchy(users, max_depth)
        all_parents_hierarchies = {}
        
        try:
            # Get the user instance from the specified username
            user_instance = MyUser.objects.get(username=user)
            # Get parents from bottom to root
            parents = cls.get_parents_bottom_to_root(user_instance)
            # Store the parent details only for the specified user
            all_parents_hierarchies[user] = parents
            userParent = all_parents_hierarchies[user][:5]
            # Call post_points with the user instance and hierarchy details
            productPrice = product_instance
            cls.create_weekend_bonus(user_instance, userParent, productPrice, parents)
        except MyUser.DoesNotExist:
            print(f"User '{user}' does not exist.")

        return all_parents_hierarchies
    

    @classmethod
    def matching_bonus_hierarchies(cls, user, max_depth=0,):
        users = cls.get_all_users()
        user_hierarchies = cls.build_user_hierarchy(users, max_depth)
        all_parents_hierarchies = {}
        
        try:
            # Get the user instance from the specified username
            user_instance = MyUser.objects.get(username=user)
            # Get parents from bottom to root
            parents = cls.get_parents_bottom_to_root(user_instance)
            # Store the parent details only for the specified user
            all_parents_hierarchies[user] = parents
            # Call post_points with the user instance and hierarchy details
           
           # cls.create_weekend_bonus(user_instance, userParent, parents)
        except MyUser.DoesNotExist:
            print(f"User '{user}' does not exist.")

        return all_parents_hierarchies

"""def process_weekend_bonus(request, max_depth):
    if request.method == 'POST':
        if 'weekend_process' in request.POST:
            # Call the static method from the BonusPay class
            BonusPay.weekend_all_user_hierarchies(max_depth)
            return HttpResponse('Processing complete')
    HttpResponse("All pending transactions processed and amounts aggregated successfully.")  # Render the template with the button
"""
def process_weekend_bonus(user, max_depth, product_instance):
    BonusPay.weekend_all_user_hierarchies(user,max_depth,product_instance)


def process_and_hierarchies(request, max_depth):
        # Call the static method from the BonusPay class
        BonusPay.print_all_user_hierarchies(max_depth)
        return HttpResponse('Processing complete')

def process_points(user, max_depth, product_instance):
    BonusPay.points_hierarchies(user,max_depth,product_instance)

def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            # Check if user with this username already exists
            if MyUser.objects.filter(username=username).exists():
                return redirect('user_detail',pk=request.user.pk)
            else:
                user_instance = form.save(commit=False)
                password = form.cleaned_data['password']
                user_instance.set_password(password)

                send_mail(
                    'Your Account Information',
                    f'Username: {username}\nPassword: {password}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                if request.user.is_authenticated:
                    user_instance.parent = request.user

                user_instance.save()

                if request.user.is_authenticated:
                    parent_node = UserNode(request.user, relationship='parent')
                    children_under_parent = MyUser.objects.filter(parent=request.user)
                    
                    for child in children_under_parent:
                        parent_node.add_child(child, relationship='child')
                        fetch_and_add_children(parent_node.children[-1], max_depth=10)

                        hierarchy_data = parent_node.show_hierarchy(max_depth=10)
                
                # Redirect to user detail page after successful creation
                return redirect('user_detail',pk=request.user.pk)
        # If form is not valid, re-render the form with errors
    else:
        # Determine which form template to render based on the URL or some condition
        if request.path == '/home/user_detials.html':  # Adjust condition based on actual URL
            form = CreateUserForm()
            template = 'home/user_detials.html'
        else:
            form = CreateUserForm()
            template = 'home/UserRegistration.html'

    return render(request, template, {
        'form': form,
        'recruit': form, })



@login_required(login_url="/login/")
def user_detail(request):
    approval_pass = random_works()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #usercode = form.cleaned_data.get(approval_pass)

            if MyUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists. Please choose a different username.'}, status=400)

            # Create a new user instance and set the password
            user_instance = form.save(commit=False)
            user_instance.set_password(password)
            user_instance.usercode = approval_pass
            approval = approval_pass


            # Send the account information email
            send_mail(
                'Your Account Information',
                f'Welcome to Lifeplus. Use the below information to access your account:\n Username: {username}\nPassword: {password}\n Approval Password: {approval}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            if request.user.is_authenticated:
                user_instance.parent = request.user
            user_instance.save()

            parent_node = UserNode(request.user, relationship='parent')
            children_under_parent = MyUser.objects.filter(parent=request.user)
                
            for child in children_under_parent:
                parent_node.add_child(child, relationship='child')
                fetch_and_add_children(parent_node.children[-1], max_depth=10)

            hierarchy_data = parent_node.show_hierarchy(max_depth=10)

            return JsonResponse({'success': True, 'redirect_url': reverse('apps_home:user_create_info', kwargs={'pk': user_instance.pk})})

        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    else:
        # GET request handling
        orders = Orders.objects.filter(user=request.user.id).values(
            'order_id',
            'order_date',
            'package_id__package_name',
            'package_id__package_price',
        ).last()
        account = Account.objects.filter(acc_holder=request.user.id, acc_type_id__in=[1,2]).values(
            'acc_type_id__name',
            'cur_bal',
        )
        parent_node = UserNode(request.user, relationship='parent')
        children_under_parent = MyUser.objects.filter(parent=request.user)
        
        for child in children_under_parent:
            parent_node.add_child(child, relationship='child')
            fetch_and_add_children(parent_node.children[-1], max_depth=10)
        
        hierarchy_data = parent_node.show_hierarchy(max_depth=10)
        form = CreateUserForm()  # Initialize form for GET request

        # Render the genealogy HTML separately
        genealogy_html = generate_html_from_hierarchy(hierarchy_data)
        childof = hierarchy_data.get('children', [])
        getId = []
        # Check if 'childof' is not empty before accessing its first element
        if childof:
            for child in childof:  # Rename the loop variable for clarity
                child_user = child.get('user')  # Get the 'user' key from the child
                if child_user:  # Only proceed if the user exists
                    user_data = MyUser.objects.filter(username=child_user).values()
                    getId.extend(user_data)  # Add the user data to the list
        else:
            # Handle the case where 'children' is empty
            getId = None

        
        def get_user_points(user_id):
            try:
                userPoints = PointsModel.objects.get(member=user_id)
                return userPoints
            except ObjectDoesNotExist:
                return None

        # Usage
        userPoints = get_user_points(request.user.id)
        member = MyUser.objects.get(username=request.user)
        return render(request, 'home/user_details.html', {
            'hierarchy': hierarchy_data,
            'form': form,
            'orders': orders,
            'account': account,
            'genealogy_html': genealogy_html,
            'childid': getId,
            'userPoints': userPoints,
            'member':member,
        })

def create_user_details(request, pk):
    products = Products.objects.all().values()  # Assuming Products model exists
    user = get_object_or_404(MyUser, pk=pk)  # Retrieve user by primary key
    acctype = AccType.objects.get(id='4')
    acctypeOpen = AccType.objects.get(id='1')
    acctypebonus = AccType.objects.get(id='2')
    myAccount = Account.objects.filter(acc_holder=request.user, acc_type_id='1').values('acc_type_id__name', 'cur_bal')
    form = keyBonusUpdate()
    parentform = ParentUpdate()
    orderForm = OrderForm(initial={'user': user.pk})
    trans = TransferFundsForm()
    main_user = request.user
    bonusUser = user.keyBonus
    admin_tb_account= admin_account = MyUser.objects.get(pk=1)
    #tb = admin_account['username']
    if bonusUser is not None:
        keybonus = get_object_or_404(MyUser, username=bonusUser)
    else:
        # Handle the case where bonusUser is None, if needed
        keybonus = None

    searched_user = None
    parent_user = None
    if request.method == 'POST':
        if 'search_button' in request.POST:
            form = keyBonusUpdate(request.POST)
            if form.is_valid():
                keyBonus_username = form.cleaned_data['keyBonus']
                try:
                    searched_user = MyUser.objects.get(username=keyBonus_username)
                except MyUser.DoesNotExist:
                    messages.error(request, f'User with username "{keyBonus_username}" does not exist.')
        elif 'save_button' in request.POST:
            keyBonus_username = request.POST.get('keyBonus_username')
            try:
                user.keyBonus = keyBonus_username
                user.save()
                messages.success(request, f'Key Bonus updated successfully for user "{user.username}".')
            except MyUser.DoesNotExist:
                messages.error(request, f'User with username "{keyBonus_username}" does not exist.')
        elif 'search_usercode' in request.POST:
            parentform = ParentUpdate(request.POST)
            if parentform.is_valid():
                usercode = parentform.cleaned_data['usercode']
                try:
                    parent_user = MyUser.objects.get(usercode=usercode)
                except MyUser.DoesNotExist:
                    messages.error(request, f'User with Member ID "{usercode}" does not exist.')
        elif 'save_usercode' in request.POST:
            usercode = request.POST.get('usercode_parent')
            userParent = MyUser.objects.get(username = usercode)
            try:
                user.parent = userParent
                user.save()
                messages.success(request, f'Key Bonus updated successfully for user "{user.username}".')
            except MyUser.DoesNotExist:
                messages.error(request, f'User with username "{keyBonus_username}" does not exist.')

        elif 'complete_recruit' in request.POST:
            
            if keybonus == None:
                keybonus = main_user
            else:
                pass
            orderForm = OrderForm(request.POST)
            if orderForm.is_valid():
                order = orderForm.save(commit=False)
                order.main_user = keybonus
                order.main_user_bonus = main_user
                order.admin_account = admin_tb_account
                package = orderForm.cleaned_data['package']
                product_instance = get_object_or_404(Products, product_id=package.product_id)
                productpoints = product_instance.product_id
                package_price = product_instance.package_price
                package_name = product_instance.package_name
                source_acc_type = get_object_or_404(Account, acc_holder=request.user,acc_type=1)
                try:
                    source_account = Account.objects.get(acc_holder=request.user, acc_type=source_acc_type.acc_type)
                    
                    if source_account.cur_bal < package_price:
                        messages.error(request, 'Insufficient balance to complete the order.')
                    else:
                        with db_transaction.atomic():
                            # Create the transaction for the order
                            Transaction.objects.create(
                                accType=acctype,
                                order_date=timezone.now(),
                                user=user,
                                tran_code=Transaction_codes.objects.get(tran_code=100),
                                desc=f'Txn2 - {package_name} - {Transaction_codes.objects.get(tran_code=100).tran_bonus.bonus}',
                                amount=package_price,
                            )
                            
                            # Create the main account transaction
                            mainaccount = Transaction.objects.create(
                                accType=acctypeOpen,
                                order_date=timezone.now(),
                                user=user,
                                tran_code=Transaction_codes.objects.get(tran_code=100),
                                desc=f'Txn1 - {package_name} {Transaction_codes.objects.get(tran_code=100).tran_bonus.bonus}',
                                amount=Decimal(0.00)
                            )
                            # Optionally, create a corresponding credit transaction for record-keeping
                            Transaction.objects.create(
                                accType=source_acc_type.acc_type,
                                user=main_user,
                                amount=-package_price,
                                desc='Order Payment',
                                tran_code=Transaction_codes.objects.get(tran_code=200)  # Example code for deduction
                            )


                            points_instance, created = PointsModel.objects.get_or_create(
                                member=user,
                                #product=product_instance,
                                defaults={'points': 0}  # Set points to 0 only if a new object is created
                            )

                            if not created:
                                # If the instance was not created, it exists, so update the points
                                points_instance.points += 1  # Or whatever logic you have to update points
                                points_instance.save() 
                            
                            # Update status of the order and save it
                            order.package = package
                            user.my_status = 'active'
                            user.save()
                            order.save()
                            process_points(user, max_depth=3, product_instance=product_instance,)
                            process_weekend_bonus(user, max_depth=3, product_instance=product_instance,)
                            
                            messages.success(request, f'Order created successfully for user "{user.username}".')
                except Account.DoesNotExist:
                    messages.error(request, 'Source account does not exist.')
                except Exception as e:
                    messages.error(request, f'An error occurred: {str(e)}')

            else:
                messages.error(request, 'Order form is not valid.')

    return render(request, 'home/user_details_create.html', {
        'products': products,
        'user': user,
        'form': form,
        'searched_user': searched_user,
        'myAccount': myAccount,
        'product_form': orderForm,
        'tran': trans,
        'parentform': parentform,
        'parent_user': parent_user,
    })

class ProductView(CreateView):
    model = Products
    template_name = 'home/billing.html'
    success_url = reverse_lazy('apps_home:dashboard')
    form_class = CreateProducts 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['product_form'] = CreateProducts()
        context['product_data'] = {
            'products': Products.objects.all().values(),
        }
        return context
    def get_template_names(self):
        if self.request.GET.get('template') == 'alternative':
            return ['home/alternative_billing.html']
        else:
            return [self.template_name]

class ProductDetials(DetailView):
    model = Products
    template_name = 'home/productDetials.html'
    success_url = reverse_lazy('apps_home:dashboard')
    form_class = CreateProducts 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productID = self.object.pk
        productDetials = Products.objects.filter(product_id=productID).values(
            'bonus__bonus',
            'bonus__occurance__occurrence_type',
            'bonus__percentage',
            'package_name',
            'package_price'
            ),
        # Combine queryset data from multiple models
        context['product_form'] = CreateProducts()
        context['product_data'] = {
            'productsDetail': productDetials
        }
        return context

class ClientProductDetail(LoginRequiredMixin, DetailView):
    model = Products
    template_name = 'home/productPurchase.html'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        order_details = Orders.objects.filter(user=user).last()  # Get the last order

        if not order_details:
            messages.error(request, 'No order found to update.')
            #return self.render_to_response(self.get_context_data())

        purchase_form = OrdersUpdateForm(request.POST, instance=order_details)

        if purchase_form.is_valid():
            try:
                source_account = get_object_or_404(Account, acc_holder=user, acc_type=1)

                if source_account.cur_bal < product.package_price:
                    messages.error(request, 'Insufficient balance to complete the order.')
                    return self.render_to_response(self.get_context_data(form=purchase_form))

                with db_transaction.atomic():
                    # Update the package in the order
                    order_details.package = product  # Set the new package
                    order_details.save()  # Save the updated order

                    # Create the transaction for the order with a negative amount
                    acctype = AccType.objects.get(id='1')
                    Transaction.objects.create(
                        accType=acctype,
                        order_date=timezone.now(),
                        user=user,
                        tran_code=Transaction_codes.objects.get(tran_code=100),
                        desc=f'Txn2 - {product.package_name} - {Transaction_codes.objects.get(tran_code=100).tran_bonus.bonus}',
                        amount=-product.package_price,  # Posting a negative value
                    )

                    messages.success(request, f'Order updated successfully for user "{user.username}".')

            except Account.DoesNotExist:
                messages.error(request, 'Source account does not exist.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Order form is not valid.')

        # Render the same template with the form and messages
        return render(request, self.template_name, {'form': purchase_form, 'product': product})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_details = Orders.objects.filter(user=self.request.user).last()

        context['product_form'] = CreateProducts()  # Assuming this is defined elsewhere
        context['order_form'] = OrdersUpdateForm(instance=order_details) if order_details else OrdersUpdateForm()
        
        product_details = Products.objects.filter(product_id=self.object.pk).values(
            'bonus__bonus',
            'bonus__occurance__occurrence_type',
            'bonus__percentage',
            'package_name',
            'package_price'
        )
        context['product_data'] = {
            'productsDetail': product_details
        }
        return context
    

class TransactionDetail(LoginRequiredMixin, FormView):
    template_name = 'home/transactionList.html'
    form_class = TransactionForm
    login_url = '/login/'

    now = timezone.now()
    start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = (start_date.replace(month=now.month+1, day=1) - timezone.timedelta(days=1)) if now.month != 12 else start_date.replace(year=now.year+1, month=1, day=1) - timezone.timedelta(days=1)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'source_user': self.request.user.pk}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getbonus = Transaction.objects.filter(tran_code = (150,100), order_date__range=(self.start_date, self.end_date) ).values()
        user = self.request.user
        mainFloat = Transaction.objects.filter(user=user, accType_id=1).values(
            'order_date', 'accType_id', 'desc', 'product_id', 'product__package_name', 'amount', 'tran_code', 'id'
        )
        bonusFloat = Transaction.objects.filter(user=user, accType_id=2).values(
            'order_date', 'accType_id', 'desc', 'product_id', 'product__package_name', 'amount', 'tran_code', 'id'
        )
        package = Transaction.objects.filter(user=user, accType_id=3).values(
            'order_date', 'accType_id', 'desc', 'product_id', 'product__package_name', 'amount', 'tran_code', 'id'
        ).last()
        mainFloataccount = Account.objects.filter(acc_holder=user, acc_type=1).values('acc_type__name', 'cur_bal')
        bonusFloataccount = Account.objects.filter(acc_holder=user, acc_type=2).values('acc_type__name', 'cur_bal').all()
        mainOrder = Orders.objects.filter(user=user).values('package__package_name', 'package__package_price').last()

        context.update({
            'mainFloat': mainFloat,
            'bonusFloat': bonusFloat,
            'package': package,
            'mainFloataccount': mainFloataccount,
            'bonusFloataccount': bonusFloataccount,
            'mainOrder': mainOrder,
        })
        return context

    def form_invalid(self, form):
        errors = form.errors.as_json()
        # Convert the JSON errors string to a dictionary
        errors_dict = json.loads(errors)
        # Extract only the "message" fields
        messages = {}
        for field, error_list in errors_dict.items():
            messages[field] = [error.get('message', '') for error in error_list]
        return JsonResponse({'messages': messages})

    def form_valid(self, form):
        user = get_object_or_404(MyUser, pk=self.request.user.pk)
        source_acc_type = form.cleaned_data['source_acc_type']
        destination_acc_type = form.cleaned_data['destination_acc_type']
        amount = form.cleaned_data['amount']
        
        retries = 3
        for attempt in range(retries):
            try:
                with db_transaction.atomic():
                    if source_acc_type == destination_acc_type:
                        raise ValueError("Source and destination account types must be different.")

                    source_account = Account.objects.get(acc_holder=user, acc_type=source_acc_type)
                    destination_account = Account.objects.get(acc_holder=user, acc_type=destination_acc_type)

                    if source_account.cur_bal < amount:
                        raise ValueError("Insufficient balance.")

                    Transaction.objects.create(
                        accType=AccType.objects.get(id=source_acc_type.id),
                        user=user,
                        amount=-amount,
                        desc = 'E-Transfer',
                        tran_code=Transaction_codes.objects.get(tran_code=350)
                    )

                    Transaction.objects.create(
                        accType=AccType.objects.get(id=destination_acc_type.id),
                        user=user,
                        amount=amount,
                        tran_code=Transaction_codes.objects.get(tran_code=100)
                    )

                return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})
            except OperationalError:
                if attempt < retries - 1:
                    time.sleep(1)  # Wait before retrying
                else:
                    raise  # Reraise the exception if max retries are exceeded

        # This line should not be reached
        raise Exception("Failed to complete the transaction after multiple attempts.")

    def get_success_url(self):
        return reverse('apps_home:transactionDetail', kwargs={'pk': self.request.user.pk})
    

class FundTransfer(LoginRequiredMixin, FormView):
    template_name = 'home/fundAccount.html'
    form_class = FundForm
    login_url = '/login/'
    success_url = reverse_lazy('apps_home:user_detail')
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        accType = AccType.objects.get(id=1)
        tran_code = Transaction_codes.objects.get(tran_code=350)
          # Fetch the AccType instance you need
        kwargs['user'] = self.request.user
        kwargs['accType'] = accType
        kwargs['tran_code'] = tran_code
        return kwargs

    def form_valid(self, form):
        # Process the form here
        transaction = form.save(commit=False)
        transaction.user = self.request.user  # Ensure the user is set
        transaction.save()
        return redirect(reverse_lazy('apps_home:user_detail'))  # Redirect to a success page or another view

    def form_invalid(self, form):
        # Handle the case when form is invalid
        return self.render_to_response(self.get_context_data(form=form))



def get_current_balance(request, acc_type_id):
    
    account = Account.objects.filter(acc_type_id=acc_type_id,acc_holder=request.user).first()
    cur_bal = account.cur_bal if account else None
    return JsonResponse({'cur_bal': str(cur_bal) if cur_bal is not None else '0.00'})
    
