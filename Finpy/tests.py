from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from Finpy.models import UserProfile
from django.core.urlresolvers import reverse

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

	def test_login(self):

		"""Método que realiza um assert para verificar
		a conformidade entre requisição da página de login
		e obtenção da mesma.
		"""

		response_login = self.client.get('/finpy/login/')
		self.assertEqual(response_login.status_code, 200)

	def test_signup(self):

		"""Método que realiza um assert para verificar
		a conformidade entre requisição da página de cadastro 
		e obtenção da mesma.
		"""

		response_signup = self.client.get('/finpy/signup/')
		self.assertEqual(response_signup.status_code, 200)

	def test_entry_create(self):

		"""Método que realiza um assert para verificar
		a conformidade entre requisição da página de lançamento
		de receitas e despesas e a obtenção da mesma.
		"""

		response_entry_create = self.client.get('/finpy/entry/create/')
		self.assertEqual(response_entry_create.status_code, 302)

	def test_entry_list(self):

		"""Método que realiza um assert para verificar
		a conformidade entre requisição da página de listagem 
		de receitas e despesas lançadas e a obtenção da mesma.
		"""

		response_entry_list = self.client.get('/finpy/entry/list/')
		self.assertEqual(response_entry_list.status_code, 302)

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
