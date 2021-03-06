from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from Finpy.models import UserProfile
from Finpy.models import InvestmentSimulation, SimulationAbstractStrategy, Entry, Category

# Create your tests here.

class FinpyViewsTestCase(TestCase):

    """Classe que possui os métodos de teste 
    para as principais urls do sistema EqLibra.
    """
    
    # HTTP code when the requested page is found
    RESPONSE_PAGE_FOUND = 302
    RESPONSE_OK = 200

    def setUp(self):
        # Creating test user profile. The UserProfile requires a Django User

        self.user1_password = 'chuck'
        user1 = User.objects.create_user(username='Chuck', password=self.user1_password)
        self.user_profile = UserProfile.objects.create(user=user1, cpf="12345678912")

        self.user2_password = 'john'
        user2 = User.objects.create_user(username='John', password=self.user2_password)
        self.user_profile2 = UserProfile.objects.create(user=user2, cpf="98765432198")

        self.category = Category.objects.create(category_name="Test Category",
                                           category_description="Test category description")

        self.user1_entry = Entry.objects.create(entry_source="Test Source", entry_value="10000",
                                           entry_due_date="2019-03-29",
                                           entry_periodicity=_('Monthly'),
                                           entry_registration_date="2019-03-20",
                                           entry_description="Test user 1 entry description",
                                           entry_quota_amount="10", entry_type=_('Income'),
                                           category=self.category, entry_user=user1)

        self.user2_entry = Entry.objects.create(entry_source="Test Source 2", entry_value="100002",
                                           entry_due_date="2019-05-29",
                                           entry_periodicity=_('Monthly'),
                                           entry_registration_date="2019-05-20",
                                           entry_description="Test user 2 entry description",
                                           entry_quota_amount="5", entry_type=_('Income'),
                                           category=self.category, entry_user=user2)

    def test_login(self):

        """Método que realiza um assert para verificar
        a conformidade entre requisição da página de login
        e obtenção da mesma.
        """

        response_login = self.client.get('/finpy/login/')
        self.assertEqual(response_login.status_code, self.RESPONSE_OK)

    def test_signup_get_view(self):
        """ Test if the signup view respond correctly when using GET method """

        url_to_test = reverse('signup')

        response = self.client.get(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        # Check if the register button is present
        self.assertIn(_('Signup'), str(response.content))
    
    def test_signup_post_view(self):
        """ Test if the signup view respond correctly when using POST method """

        url_to_test = reverse('signup')

        post_data = {
            'username': "testuser",
            'first_name': "Test User",
            'last_name': "LastName",
            'email': "testuser@mail.com",
            'password1': "testuser",
            'password2': "testuser",
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        # Check if the user was registered
        user = User.objects.get(username=post_data['username'])
        self.assertEqual(user.username, post_data['username'])
        self.assertEqual(user.first_name, post_data['first_name'])
        self.assertEqual(user.email, post_data['email'])

    def test_about_page(self):

        """ Test the about view """

        response_entry_list = self.client.get(reverse('about'))
        self.assertEqual(response_entry_list.status_code, self.RESPONSE_OK)

    def test_service_page(self):

        """ Test the service descriptions view """

        response_entry_list = self.client.get(reverse('services_description'))
        self.assertEqual(response_entry_list.status_code, self.RESPONSE_OK)

    def test_simulation_list(self):

        """ Test the simulation list view """

        response_entry_list = self.client.get(reverse('list_simulations'))
        self.assertEqual(response_entry_list.status_code, self.RESPONSE_PAGE_FOUND)
    
    def test_entry_list(self):

        """ Test the list entry view """

        response_entry_list = self.client.get(reverse('list_entry'))
        self.assertEqual(response_entry_list.status_code, self.RESPONSE_PAGE_FOUND)     

    def test_update_profile_get_view(self):
        """ Test if the profile view respond correctly when using GET method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('update_profile', kwargs={'profile_id': self.user_profile.user.id})

        update_profile_response = self.client.get(url_to_test, follow=True)
        self.assertEqual(update_profile_response.status_code, self.RESPONSE_OK)

        # If the CPF of the logged user appears on the page, the request was sucessfully done
        self.assertIn(self.user_profile.cpf, str(update_profile_response.content))
    
    def test_update_another_person_profile_get_view(self):
        """ Test if the profile view respond correctly when trying to access 
            another person profile using GET method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        # Trying to access the update profile page of user 2
        url_to_test = reverse('update_profile', kwargs={'profile_id': self.user_profile2.user.id})

        update_profile_response = self.client.get(url_to_test, follow=True)
        self.assertEqual(update_profile_response.status_code, self.RESPONSE_OK)

        # If this text appear on the response page, the system 
        #  did not let the user update another profile
        expected_message = _("This isn't your profile")
        self.assertIn(expected_message, str(update_profile_response.content, 'utf-8'))

    def test_update_profile_post_view(self):
        """ Test if the profile view respond correctly when using POST method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('update_profile', kwargs={'profile_id': self.user_profile.user.id})

        # Trying to update the user CPF to 98745678345
        new_cpf = "98745678345"
        post_data = {
            'profile_id': self.user_profile.user.id,
            'cpf': new_cpf
        }

        update_profile_response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(update_profile_response.status_code, self.RESPONSE_OK)

        # If the new CPF appears on the page, the request was sucessfully done
        self.assertIn(new_cpf, str(update_profile_response.content))

    def test_update_another_person_profile_post_view(self):
        """ Test if the profile view respond correctly when trying to access 
            another person profile using POST method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        # Try to access the update profile page of user 2
        url_to_test = reverse('update_profile', kwargs={'profile_id': self.user_profile2.user.id})

        # Trying to update the user CPF to 98745678345
        new_cpf = "98745678345"
        post_data = {
            'profile_id': self.user_profile.user.id,
            'cpf': new_cpf
        }

        update_profile_response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(update_profile_response.status_code, self.RESPONSE_OK)

        # If this text appear on the response page, the system 
        #  did not let the user update another profile
        expected_message = _("This isn't your profile")
        self.assertIn(expected_message, str(update_profile_response.content, 'utf-8'))

    def test_simulate_investment_get_view(self):
        """ Test if the simulate investment view respond correctly when using GET method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('simulate_investment')

        response = self.client.get(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

    def test_simulate_investment_post_view(self):
        """ Test if the simulate investment view respond correctly when using POST method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('simulate_investment')

        # An arbitrary present value
        present_value = "9857484"
        post_data = {
            'present_value': present_value
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)
        self.assertIn(present_value, str(response.content))

    def test_create_entry_get_view(self):
        """ Test if the create entry view respond correctly when using GET method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('create_entry')

        response = self.client.get(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

    def test_create_entry_post_view(self):
        """ Test if the create view respond correctly when using POST method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('create_entry')

        # An arbitrary entry value
        entry_value = "99899"
        post_data = {
            'entry_value': entry_value
        }

        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)
        self.assertIn(entry_value, str(response.content))

    def test_update_entry_get_view(self):
        """ Test if the update entry view respond correctly when using GET method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('update_entry', kwargs={'entry_id': self.user1_entry.id})

        response = self.client.get(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)
        self.assertIn(self.user1_entry.entry_source, str(response.content))
        self.assertIn(self.user1_entry.entry_value, str(response.content))
        self.assertIn(self.user1_entry.entry_description, str(response.content))

    def test_update_entry_post_view(self):
        """ Test if the update entry view respond correctly when using POST1 method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        url_to_test = reverse('update_entry', kwargs={'entry_id': self.user1_entry.id})

        post_data = {
            'entry_source': "Test Source Updated",
            'entry_value': "10000.00",
            'entry_due_date': "2019-03-29", 
            'entry_periodicity': _('Monthly'), 
            'entry_registration_date': "2019-03-20",
            'entry_description': "Test user 1 entry description updated",
            'entry_quota_amount': "5",
            'entry_type': _('Income'),
            'category': self.category.id,
        }

        # Test if the post was successfully done
        response = self.client.post(url_to_test, post_data, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        # Test if the new entry data was saved
        response = self.client.get(url_to_test, follow=True)
        entry = Entry.objects.get(pk=int(self.user1_entry.id))
        self.assertEqual(post_data['entry_source'], entry.entry_source)
        self.assertEqual(post_data['entry_description'], entry.entry_description)

    def test_update_another_person_entry_get_view(self):
        """ Test if the update entry view respond correctly when trying to access 
            another person entry using GET method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        # Trying to access user2 entry
        url_to_test = reverse('update_entry', kwargs={'entry_id': self.user2_entry.id})

        response = self.client.get(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        expected_message = _("This isn't your profile")
        self.assertIn(expected_message, str(response.content, 'utf-8'))

    def test_update_another_person_entry_post_view(self):
        """ Test if the update entry view respond correctly when trying to access 
            another person entry using POST method """

        # Logging in with user 1
        logged = self.client.login(username=self.user_profile.user.username, password=self.user1_password)

        # Trying to access user2 entry
        url_to_test = reverse('update_entry', kwargs={'entry_id': self.user2_entry.id})

        # Test if the post was successfully done
        response = self.client.post(url_to_test, follow=True)
        self.assertEqual(response.status_code, self.RESPONSE_OK)

        expected_message = _("This isn't your profile")
        self.assertIn(expected_message, str(response.content, 'utf-8'))

class FinpyModelsTestCase(TestCase):

    """ Class to test models classes """

    def setUp(self):

        """ Method to create a investment simulation """
        id_simulation = 1
        present_value = 1000
        future_value = 10000
        payment_value = 100
        rate_value = 0.5
        period_value = 1
        simulation_type = InvestmentSimulation.FINANCIAL_MATH
        result_to_discover = InvestmentSimulation.FUTURE_VALUE

        self.investmentSimulation = InvestmentSimulation(id_simulation, present_value, future_value, payment_value,
                                                        rate_value, period_value, simulation_type, result_to_discover)


    def test_calculate_investment_financial_future(self):

        """ Test the method that calculates an investment that has the Financial Math 
            type and the result is the Future Value"""
        
        simulation_result = self.investmentSimulation.calculate_investment()
        expected_result = [1000]
        self.assertEqual(simulation_result, expected_result)


    def test_calculate_invesment_financial_present(self):

        """ Test the method that calculates an investment that has the Financial Math 
            type and the result is the Present Value"""
        
        self.investmentSimulation.result_to_discover = InvestmentSimulation.PRESENT_VALUE
        simulation_result = self.investmentSimulation.calculate_investment()
        expected_result = [10000]
        self.assertEqual(simulation_result, expected_result)

    def test_calculate_invesment_return_period(self):

        """ Test the method that calculates an investment that has the Investment Return 
            type and the result is the Period Value"""
        
        self.investmentSimulation.simulation_type = InvestmentSimulation.INVESTMENT_RETURN
        self.investmentSimulation.result_to_discover = InvestmentSimulation.PERIOD_VALUE
        simulation_result = self.investmentSimulation.calculate_investment()
        expected_result = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(simulation_result, expected_result)
