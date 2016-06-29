from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from Finpy.models import UserProfile, Entry, InvestmentSimulation


class UserCreationForm(forms.ModelForm):

    """UserCreationForm Class. This class contains the treatments
     of the existents forms on register user page
    """

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:

        """Meta Class. This class defines the informations
        that will be used based on existent set from
        User Model of the Django framework.
        """

        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_password2(self):
        """ Used to clean the password """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        """ Used to save the user """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class InvestmentSimulationForm(forms.ModelForm):

    """InvestmentSimulationForm Class. This class contains the treatments
     of the existents forms on investment simulation page.
    """

    class Meta:

        """Meta Class. This class defines the informations
        that will be used based on existent set
        from InvestmentSimulation Model.
        """

        model = InvestmentSimulation
        fields = '__all__'
        exclude = ['simulation_user']

class ProfileUpdateForm(forms.ModelForm):

    
    """ProfileUpdateForm Class. TThis class contains the treatments
     of the existents forms on update user information page.
    """

    class Meta:

        """Meta Class. This class defines the informations
        that will be used based on existent set
        from UserProfile Model.
        """

        model = UserProfile
        fields = '__all__'
        exclude = ['user',]

class EntryForm(forms.ModelForm):

    """EntryForm Class. This class contains the treatments
     of the existents forms on launches of revenues and expenses page.  
    """

    class Meta:

        """Meta Class. This class defines the informations
        that will be used based on existent set on Entry Model.
        """

        model = Entry
        fields = '__all__'
        exclude = ['entry_user']

    def delete(self, instance=None):
        """ Used to delete a entry """
        return instance.delete()
