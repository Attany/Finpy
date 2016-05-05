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

class UpdateProfileView(View):

    # Allowed methods on the view
    http_method_names = [u'get', u'post']

    template_name='profile/update.html'
    update_form=ProfileUpdateForm
    current_app=None
    extra_context=None

    @method_decorator(login_required)
    def get(self, request, profile_id=None):
        """ Get the previous data of the current user to update profile """

        user_auth = self.check_user(request, profile_id)
        if user_auth['authenticated']:
            form = self.update_form(instance=user_auth['profile'])

            context = self.check_extra_content(form)
            
            response = TemplateResponse(request, self.template_name, context, 
                current_app=self.current_app)
        else:
            response = HttpResponse(_("This isn't your profile"))

        return response

    @method_decorator(login_required)
    def post(self, request, profile_id=None):
        """ Update the user profile with given information """

        user_auth = self.check_user(request, profile_id)
        if user_auth['authenticated']:
            form = self.update_form(data=request.POST, instance=user_auth['profile'])
            if form.is_valid():
                form.save()

            context = self.check_extra_content(form)
            
            response = TemplateResponse(request, self.template_name, context, 
                current_app=self.current_app)
        else:
            response = HttpResponse(_("This isn't your profile"))

        return response

    def check_user(self, request, user_id):
        """ Check if the current user is the update profile request user"""

        current_user_auth = {'authenticated': False, 'profile': None}
        if user_id is not None:
            profile = UserProfile.objects.get(pk=int(user_id))
            user = profile.user
            if user == request.user:
                current_user_auth = {'authenticated': True, 'profile': profile}
            else:
                current_user_auth = {'authenticated': False, 'profile': None}

        return current_user_auth

    def check_extra_content(self, form):
        """ Checks if have extra content to add in the context """

        context = {
            'form': form,
            'title': _('User Profile Update'),
        }

        if self.extra_context is not None:
            context.update(self.extra_context)
        
        return context


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
def simulate_investment(request, template_name='investment/simulate.html',
    investment_simulation_form=InvestmentSimulationForm, current_app=None, extra_context=None):
    if request.method == "POST":
        investment_simulation = InvestmentSimulation()
        investment_simulation.simulation_user = request.user
        form = investment_simulation_form(data=request.POST, instance=investment_simulation)
        if form.is_valid():
            form.save()
    else:
        form = investment_simulation_form()

    context = {
        'form': form,
        'title': _('Investment Simulation')
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
        current_app=current_app)

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
def create_entry(request, template_name='entry/create.html',
    entry_form=EntryForm, current_app=None, extra_context=None):
    if request.method == "POST":
        entry = Entry()
        entry.entry_user = request.user
        form = entry_form(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
    else:
        form = entry_form()

    context = {
        'form': form,
        'title': _('Entry Creation')
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
