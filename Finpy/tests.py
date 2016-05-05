from django.test import TestCase
from Finpy.models import InvestmentSimulation, SimulationAbstractStrategy

# Create your tests here.

class FinpyViewsTestCase(TestCase):

    """Classe que possui os métodos de teste 
    para as principais urls do sistema EqLibra.
    """

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

        