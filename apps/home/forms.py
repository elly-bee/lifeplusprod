# forms.py
from django import forms
from .models import MyUser,Orders,Account,AccType,Transaction
from .models import Products


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username','password','first_name', 'last_name', 'dateofbirth','email', 'marital_status', 'gender', 'address', 'phone_number_1', 'phone_number_2','parent']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dateofbirth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'phone_number_1': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control', 'id': 'parent-select'}),
        }


class keyBonusUpdate(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['keyBonus']  
        widgets = {
            'keyBonus': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyBonus'].queryset = MyUser.objects.all()
        self.fields['keyBonus'].label = 'Search for user to get KeyBonus'

class ParentUpdate(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['usercode']  
        widgets = {
            'usercode': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usercode'].queryset = MyUser.objects.all()
        self.fields['usercode'].label = 'Search User Member Id to where the New User should belong to'
        
class selectAccountForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['usercode']  
        widgets = {
            'usercode': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usercode'].queryset = MyUser.objects.all()
        self.fields['usercode'].label = 'Enter the Member ID'
        


class TransferFundsForm(forms.ModelForm):
    cur_bal = forms.DecimalField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Account
        fields = ['acc_type', 'amount', 'cur_bal']
        widgets = {
            'acc_type': forms.Select(attrs={'class': 'form-control', 'id': 'acc-type-select'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acc_type'].queryset = AccType.objects.all()

    def get_current_balance(self, acc_type_id):
        try:
            account = Account.objects.filter(acc_type_id=acc_type_id).first()
            return account.cur_bal if account else None
        except Account.DoesNotExist:
            return None
        

class TransferToAccountForm(forms.Form):
    source_user = forms.ModelChoiceField(queryset=MyUser.objects.all(), label="Source User")
    destination_user = forms.ModelChoiceField(queryset=MyUser.objects.all(), label="Destination User")
    source_acc_type = forms.ModelChoiceField(queryset=AccType.objects.filter(), label="Source Account Type")
    destination_acc_type = forms.ModelChoiceField(queryset=AccType.objects.filter(pk__in=[1]), label="Destination Account Type")
    amount = forms.DecimalField(max_digits=20, decimal_places=2, min_value=0.01, label="Amount")

    """def __init__(self, *args, **kwargs):
        destination_user_queryset = kwargs.pop('destination_user_queryset', MyUser.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['destination_user'].queryset = destination_user_queryset"""
    def clean(self):
        cleaned_data = super().clean()
        source_user = cleaned_data.get("source_user")
        destination_user = cleaned_data.get("destination_user")
        source_acc_type = cleaned_data.get("source_acc_type")
        amount = cleaned_data.get("amount")

        # Validate sufficient balance
        if amount and source_acc_type:
            try:
                source_account = Account.objects.get(acc_holder=source_user, acc_type=source_acc_type)
                if source_account.cur_bal < amount:
                    raise forms.ValidationError("Insufficient balance.")
            except Account.DoesNotExist:
                raise forms.ValidationError("Source user does not have an account.")

        return cleaned_data

class CreateProducts(forms.ModelForm):
    package_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*'}))
    class Meta:
        model = Products
        fields = ['package_name','package_price','bonus']
        widgets = {
            'package_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bonus': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'

class FundForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"ZMW"}),
        }
    def __init__(self, *args, **kwargs):
        # Extract custom keyword arguments
        user = kwargs.pop('user', None)
        accType = kwargs.pop('accType', None)
        tran_code = kwargs.pop('tran_code', None)
        
        # Call the superclass constructor
        super().__init__(*args, **kwargs)
        
        # Set initial values for custom fields
        if user:
            self.fields['user'].initial = user
        if accType:
            self.fields['accType'].initial = accType
        if accType:
            self.fields['tran_code'].initial = tran_code
       


class TransactionForm(forms.Form):
    source_user = forms.ModelChoiceField(queryset=MyUser.objects.all(), label="Source User")
    #source_acc_type = forms.ModelChoiceField(queryset=AccType.objects.all(), label="Source Account Type")
    source_acc_type = forms.ModelChoiceField(queryset=AccType.objects.filter(pk__in=[2]), label="Source Account Type")
    destination_acc_type = forms.ModelChoiceField(queryset=AccType.objects.filter(pk__in=[1]), label="Destination Account Type")
    amount = forms.DecimalField(max_digits=20, decimal_places=2, min_value=0.01, label="Amount")

    def clean(self):
        cleaned_data = super().clean()
        source_user = cleaned_data.get("source_user")
        source_acc_type = cleaned_data.get("source_acc_type")
        destination_acc_type = cleaned_data.get("destination_acc_type")
        amount = cleaned_data.get("amount")

        if source_acc_type == destination_acc_type:
            raise forms.ValidationError("Source and destination account types must be different.")

        # Optional: Add more validation such as checking if the source account has sufficient balance
        if amount and source_acc_type:
            
            # Example of checking if the source user has enough balance
            try:
                source_account = Account.objects.get(acc_holder=source_user, acc_type=source_acc_type)
                if source_account.cur_bal < amount:
                    raise forms.ValidationError("Insufficient balance.")
            except Account.DoesNotExist:
                raise forms.ValidationError("Source user does not have an account.")

        return cleaned_data
    

class OrdersUpdateForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['package']