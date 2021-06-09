from django import forms

from . models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    '''use like this to include custom fields again that is not included in models or if you want to edit models'''
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "password", 'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Confirm  password", 'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password']
        '''Use widgets that is already in models'''
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
        #     'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        #     'phone_number': forms.NumberInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your phone number'
        # css class for all fields it will loop through all fields that is custom form or modelForm(database models)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password doesnot match!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={
        'invalid': {"image files only"}}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city',
                  'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
