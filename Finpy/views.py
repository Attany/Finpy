from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic import View
from Finpy.models import UserProfile, Entry, InvestmentSimulation
from Finpy.forms import UserCreationForm, ProfileUpdateForm, EntryForm, InvestmentSimulationForm

# Create your views here.

class FormContextMixin:
    """Class with common methods of form views"""
    
    template_name = ""
    form = None
    form_title = ""
    current_app = None
    extra_context = None
    context_form = None

    def get_context(self):

        context = {
            'form': self.context_form,
            'title': _(self.form_title),
        }

        if self.extra_context is not None:
            context.update(self.extra_context)
        
        return context

    def generate_template_response(self, request):

        context = self.get_context()

        response = TemplateResponse(request, self.template_name, context, 
                current_app=self.current_app)

        return response


class UpdateProfileView(View, FormContextMixin):

    # Allowed methods on the view
    http_method_names = [u'get', u'post']

    template_name = 'profile/update.html'
    form = ProfileUpdateForm
    form_title = 'User Profile Update'

    @method_decorator(login_required)
    def get(self, request, profile_id=None):
        """ Get the previous data of the current user to update profile """

        try:
            profile = self.check_user(request, profile_id)
            form = self.form(instance=profile)
            self.context_form = form
            response = self.generate_template_response(request)
        except Exception as e:        
            response = HttpResponse(str(e))

        return response

    @method_decorator(login_required)
    def post(self, request, profile_id=None):
        """ Update the user profile with given information """

        try:
            profile = self.check_user(request, profile_id)
            form = self.form(data=request.POST, instance=profile)
            if form.is_valid():
                form.save()
            self.context_form = form
            response = self.generate_template_response(request)
        except Exception as e:        
            response = HttpResponse(str(e))

        return response

    def check_user(self, request, user_id):
        """ Check if the current user is the update profile request user"""

        if user_id is not None:
            profile = UserProfile.objects.get(pk=int(user_id))
            user = profile.user
            if user == request.user:
                return profile
            else:
                raise Exception(_("This isn't your profile"))
        else:
            raise Exception(_("This isn't your profile"))



class InvestmentSimulationView(View, FormContextMixin):

    # Allowed methods on the view
    http_method_names = [u'get', u'post']

    template_name = 'investment/simulate.html'
    form = InvestmentSimulationForm
    form_title = 'Investment Simulation'

    @method_decorator(login_required)
    def get(self, request):
        """ Get the investment simulation form """

        form = self.form()
        self.context_form = form
        response = self.generate_template_response(request)

        return response

    @method_decorator(login_required)
    def post(self, request):
        """ Create an investment simulation with the given information """

        investment_simulation = InvestmentSimulation()
        investment_simulation.simulation_user = request.user
        form = self.form(data=request.POST, instance=investment_simulation)
        if form.is_valid():
            form.save()
        self.context_form = form
        response = self.generate_template_response(request)
        
        return response


class CreateEntryView(View, FormContextMixin):

    # Allowed methods on the view
    http_method_names = [u'get', u'post']

    template_name = 'entry/create.html'
    form = EntryForm
    form_title = 'Entry Creation'

    @method_decorator(login_required)
    def get(self, request):
        """ Get the investment simulation form """

        self.context_form = self.form()
        response = self.generate_template_response(request)

        return response

    @method_decorator(login_required)
    def post(self, request):
        """ Create a new entry with the given information """

        entry = Entry()
        entry.entry_user = request.user
        form = self.form(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()

        self.context_form = form
        response = self.generate_template_response(request)

        return response

def about_page(request, template_name='Finpy/about.html'):
    return TemplateResponse(request, template_name)

def service_page(request, template_name='Finpy/service.html'):
    return TemplateResponse(request, template_name)

@login_required
def index(request, template_name='Finpy/homepage.html'):
    context = {
        'profile_id': request.user.userprofile.id,
        'title': _('Home'),
    }
    return TemplateResponse(request, template_name, context)

@login_required
def list_simulations(request, template_name='investment/list.html',
    current_app=None, extra_context=None):
    simulations = request.user.investmentsimulation_set.all()
    context = {
        'simulations': simulations,
        'title': _('Investment Simulation List')
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
        current_app=current_app)

@login_required
def list_entry(request, template_name='entry/list.html',
    current_app=None, extra_context=None):
    entries = request.user.entry_set.all()
    context = {
        'entries': entries,
        'title': _('Entry List')
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
        current_app=current_app)

@login_required
def update_entry(request, entry_id=None, template_name='entry/update.html',
    success_view=list_entry, entry_form=EntryForm, current_app=None, extra_context=None):
    if entry_id is not None:
        entry = Entry.objects.get(pk=int(entry_id))
        if entry.entry_user == request.user:
            if request.method == "POST":
                form = entry_form(data=request.POST, instance=entry)
                if form.is_valid():
                    form.save()
                    return redirect(success_view)
            else:
                form = entry_form(instance=entry)

            context = {
                'form': form,
                'title': _('Entry Creation')
            }
            if extra_context is not None:
                context.update(extra_context)
            return TemplateResponse(request, template_name, context,
                current_app=current_app)
        else:
            return HttpResponse(_("This isn't your profile"))

@login_required
def delete_entry(request, entry_id=None, template_name='entry/delete.html',
    success_view=list_entry, entry_form=EntryForm, current_app=None, extra_context=None):
    if entry_id is not None:
        entry = Entry.objects.get(pk=int(entry_id))
        if entry.entry_user == request.user:
            form = entry_form(data=request.POST, instance=entry)
            form.delete(entry)
            return redirect(success_view)

        else:
            return HttpResponse(_("This isn't your profile"))

def signup(request, template_name='registration/signup.html',
    post_signup_redirect=None, signup_form=UserCreationForm,
    current_app=None, extra_context=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('login')
    else:
        post_signup_redirect = resolve_url(post_signup_redirect)
    if request.method == "POST":
        form = signup_form(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
            return HttpResponseRedirect(post_signup_redirect)
    else:
        form = signup_form()
    context = {
        'form': form,
        'title': _('User Registration'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
        current_app=current_app)
