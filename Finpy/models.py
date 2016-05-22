from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import User


class States:
    
    # Possible values for State
    AC = 'AC'
    AL = 'AL'
    AP = 'AP'
    AM = 'AM'
    BA = 'BA'
    CE = 'CE'
    DF = 'DF'
    ES = 'ES'
    GO = 'GO'
    MA = 'MA'
    MT = 'MT'
    MS = 'MS'
    MG = 'MG'
    PA = 'PA'
    PB = 'PB'
    PR = 'PR'
    PE = 'PE'
    PI = 'PI'
    RJ = 'RJ'
    RN = 'RN'
    RS = 'RS'
    RO = 'RO'
    RR = 'RR'
    SC = 'SC'
    SP = 'SP'
    SE = 'SE'
    TO = 'TO'

    # Enum of States
    STATES = (
    (AC, 'AC'),
    (AL, 'AL'),
    (AP, 'AP'),
    (AM, 'AM'),
    (BA, 'BA'),
    (CE, 'CE'),
    (DF, 'DF'),
    (ES, 'ES'),
    (GO, 'GO'),
    (MA, 'MA'),
    (MT, 'MT'),
    (MS, 'MS'),
    (MG, 'MG'),
    (PA, 'PA'),
    (PB, 'PB'),
    (PR, 'PR'),
    (PE, 'PE'),
    (PI, 'PI'),
    (RJ, 'RJ'),
    (RN, 'RN'),
    (RS, 'RS'),
    (RO, 'RO'),
    (RR, 'RR'),
    (SC, 'SC'),
    (SP, 'SP'),
    (SE, 'SE'),
    (TO, 'TO')
    )

class UserProfile(models.Model):

    """UserProfile class. This class contains information relation
    to the User Profile. Permorms extension Model provider by the
    Django framework itself with basic user information.
    """

    # User associed
    user = models.OneToOneField(User)
 
    # CPF
    cpf = models.CharField(_('cpf'),max_length=14,
        help_text=_('Use format ???.???.???-??'),
        validators=[
            validators.RegexValidator(r'^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}$',_('Wrong Format!'), 'invalid'),
        ], blank=True)
    
    # Profession
    job_title = models.CharField(_('Job Title'), max_length=150, blank=True)
    
    # Organization whick works
    organization = models.CharField(_('Organization'), max_length=150, blank=True)

    # Estado do Orgao Expedidor do RG
    expeditor_uf = models.CharField(_('Expeditor'),max_length=2, choices=States.STATES, default=States.DF, blank=True)
    
    # RG
    rg = models.CharField(_('rg'),max_length=9,
        help_text=_('Use format ?.???.???'),
        validators=[
                validators.RegexValidator(r'^[0-9]{1}\.?[0-9]{3}\.?[0-9]{3}$',_('Wrong Format!'), 'invalid'),
        ], blank=True)

    
    def __str__(self):
        
        """This method is responsible for converting to the format string.
        """

        return self.user.username



class Finance(models.Model):

    """Classe Finance. This class contains information relating to posting
    of revenues and expenses, such as frequency, linking an entry to a particular
    user and capital values.
    """

    # User associate
    finance_user = models.OneToOneField(User)

    # Total value of entry
    total_entry_value = models.DecimalField(_('Total Entry Value'), decimal_places=2, max_digits=12)
    
    # Current value
    current_value = models.DecimalField(_('Current Entry Value'), decimal_places=2, max_digits=12)

    # Frequency of possible values
    UNDEFINED = _('Undefined')
    DAILY = _('Daily') # day
    WEEKLY = _('Weekly') # week
    MONTHLY = _('Monthly') # month

    # Frequency of Enum
    PERIODICITY = (
    (UNDEFINED, _('Undefined')),
    (DAILY, _('Daily')),
    (WEEKLY, _('Weekly')),
    (MONTHLY, _('Monthly')),
    )

    def __str__(self):
        
        """This method is responsible for converting to the format string.
        """

        return self.current_value

class InvestmentSimulation(models.Model):

    """Class InvestmentSimulation. This class has the inherent information to
    investment simulations, both in Financial Mathematics, but also from the 
    perspective of Investment Return Analysis.
    """

    # Present value of the investment
    present_value = models.DecimalField(_('Valor Presente'), decimal_places=2, max_digits=12, blank=True, null=True)

    # Future value of the investment
    future_value = models.DecimalField(_('Valor Futuro'), decimal_places=2, max_digits=12, blank=True, null=True)

    # Payment value used in the simulation
    payment_value = models.DecimalField(_('Valor do Pagamento'), decimal_places=2, max_digits=12, blank=True, null=True)
 
    # Rate value
    rate_value = models.DecimalField(_('Valor da Taxa'), decimal_places=2, max_digits=3, blank=True, null=True)   
    
    # Duration time investment
    period_value = models.PositiveIntegerField(_('Valor do Período'), default=1, blank=True, null=True)

    # Identify items Enum
    PRESENT_VALUE = _('Present Value')
    FUTURE_VALUE = _('Future Value')
    PERIOD_VALUE = _('Period Value')

    # Identify the type of result Enum
    RESULT_TO_DISCOVER = (
    (PRESENT_VALUE, _('Valor Presente')),
    (FUTURE_VALUE, _('Valor Futuro')),
    (PERIOD_VALUE, _('Valor do Período')),
    )

    # Items of the type of simulation Enum
    FINANCIAL_MATH = _('Financial Math')
    INVESTMENT_RETURN = _('Investment Return')

    # Type of simulation Enum
    SIMULATION_TYPE = (
    (FINANCIAL_MATH, _('Matemática Financeira')),
    (INVESTMENT_RETURN, _('Retorno de Investimento')),
    )

    # Define investment type
    simulation_type = models.CharField(_('Tipo de Simulação'), choices=SIMULATION_TYPE, default=FINANCIAL_MATH, max_length=30)

    # Define result to discover
    result_to_discover = models.CharField(_('Resultado a Descobrir'), choices=RESULT_TO_DISCOVER, default=FUTURE_VALUE, max_length=30)

    simulation_user = models.ForeignKey(User, verbose_name=_('User'))

    def calculate_investment(self):
        
        """This method checks the user after simulation parameters and trigger
        the appropriate method for calculatin one of the elements belonging to
        modules of Economic Engineering (Financial Mathematics of Investment)
        """

        return SimulationAbstractStrategy.calculate_investment(self)

    def __str__(self):

        """This method is responsible for converting to the format string.
        """

        return str(self.present_value)

class SimulationAbstractStrategy:

    """SimulationAbstractStrategy class. Abstratct class built for the application
    of GoF Design Patterns Behavioral Template Method and Strategy. It has the
    signature of the definition of validation methods and methods of construction steps
    for investment simulation operations.
    """
    def calculate_investment_financial_math(simulation_investment):
        
        """ Calculates the investments simulation for Financial Math type. """

        if simulation_investment.result_to_discover == InvestmentSimulation.PRESENT_VALUE:
            result_list = PresentValueStrategy.calculate_steps(simulation_investment)
            PresentValueStrategy.validate_result(simulation_investment,result_list[-1])
        elif simulation_investment.result_to_discover == InvestmentSimulation.FUTURE_VALUE:
            result_list = FutureValueStrategy.calculate_steps(simulation_investment)
            FutureValueStrategy.validate_result(simulation_investment,result_list[-1])
        else:
            result_list = []

        return result_list

    def calculate_investment_return_investment(simulation_investment):

        """ Calculates the investments simulation for Investment Return type. """

        if simulation_investment.result_to_discover == InvestmentSimulation.PERIOD_VALUE:
            result_list = PayBackStrategy.calculate_steps(simulation_investment)
            PayBackStrategy.validate_result(simulation_investment, result_list[0])
        else:
            result_list = []

        return result_list

    def calculate_investment(simulation_investment):

        """Method that, given an instance of InvestmentSimulation, checks the Economic
        Engineering. In The case of Financial Mathematics for example, depending on the
        user populated fields, it can be calculated present value or future value. Within 
        Investment Return Analysis, have been calculating the payback period (return time
        of investment).
        """
        if simulation_investment.simulation_type == InvestmentSimulation.FINANCIAL_MATH:
            result_list = SimulationAbstractStrategy.calculate_investment_financial_math(simulation_investment)
        
        elif simulation_investment.simulation_type == InvestmentSimulation.INVESTMENT_RETURN:
            result_list = SimulationAbstractStrategy.calculate_investment_return_investment(simulation_investment)

        return result_list


    def calculate_steps(simulation_investment): pass

    def validate_result(simulation_investment,result): pass

class PresentValueStrategy(SimulationAbstractStrategy):

    """PresentValueStrategy class. This class in the extension of SimulationAbstractStrategy
    and formalizes class all behaviors in the Present Value calcularion.
    """

    def calculate_steps(simulation_investment):

        """Method that populates a list with the results of each iterarion of the present
        value calculation.
        """

        result = fv = simulation_investment.future_value
        period = simulation_investment.period_value
        rate = simulation_investment.rate_value/100
        result_list = [fv]
        for k in range(1, period):
            result = fv/((1 + rate)**k)
            result_list.append(result)
        return result_list

    def validate_result(simulation_investment,result):

        """Method that checks if the last value of the present value of the
        present value calculations iteration matches the direct application
        of the equation for the givem application.
        """

        fv = simulation_investment.future_value
        period = simulation_investment.period_value
        rate = simulation_investment.rate_value/100
        return fv/((1 + rate)**period) == result


class FutureValueStrategy(SimulationAbstractStrategy):

    """FutureValueStrategy Class. This class realizes the extent of 
    SimulationAbstractStrategy class and formalizes all behaviours in
    the calculation of the Future Value.
    """

    def calculate_steps(simulation_investment):

        """Method that populates a list with the result of each
        iteration of the calculation of the Future Value.
        """

        result = pv = simulation_investment.present_value
        period = simulation_investment.period_value
        rate = simulation_investment.rate_value/100
        result_list = [pv]
        for k in range(1, period):
            result += (result*rate)
            result_list.append(result)
        return result_list

    def validate_result(simulation_investment,result):

        """Method tha checks if the last value of iteration calculations
        Future Value is in accordance with the direct application of the 
        equation for the given period.
        """

        pv = simulation_investment.present_value
        period = simulation_investment.period_value
        rate = simulation_investment.rate_value/100
        return pv*((1 + rate)**period) == result


class PayBackStrategy(SimulationAbstractStrategy):

    """PayBackStrategy class. This class realizes the extent of 
    SimulationAbstractStrategy class and formalizes all behaviors related
    to the calculation of payback.
    """

    def calculate_steps(simulation_investment):
    	pv = simulation_investment.present_value
    	pmt = simulation_investment.payment_value
    	result_list = [pv/pmt]
    	pv -= pmt
    	while pv > 0:
    		result_list.append(pv/pmt)
    		pv -= pmt
    	return result_list

    def validate_result(simulation_investment,result):

        """Method that implements the direct calcularion to verify the simple
        PayBack for a particular investment.
        """

        pv = simulation_investment.present_value
        pmt = simulation_investment.payment_value
        return pv/pmt == result


class Category(models.Model):

    """Category class. This class has information related to the maintenance
    of revenue and expense categories.
    """

    # Name of category recorded
    # Name of category never should be blank
    category_name = models.CharField(_('Name Category'), max_length=30, blank=False)

    # Detail of category recorded
    # Is not required
    category_description = models.TextField(_('Description Category'), max_length=150, blank=True)

    # Type of entry
    INCOME = _('Income')
    EXPENSE = _('Expense')

    # Enum entry
    ENTRY_TYPE = (
    (INCOME, _('Income')),
    (EXPENSE, _('Expense')),
    )

    def __str__(self):

        """This method is responsible for converting to the format string.
        """

        return self.category_name

class Entry(models.Model):

    """Entry class. This class has detailed information for a particular
    entry, may be income or expense.
    """

    # Company or Organization source Launch of request
    entry_source = models.CharField(_('Entry Source'), max_length=50, blank=True)

    # Registry of the value entry
    entry_value = models.DecimalField(_('Entry Value'), decimal_places=2, max_digits=12)
    
    # Due date
    entry_due_date = models.DateField(_('Due Date'))

    # Registry of the entry registration date
    entry_registration_date = models.DateField(_('Registration Date'))

    # Entry description
    entry_description = models.TextField(_('Entry Description'), max_length=150, blank=True)

    # Quota quantity
    entry_quota_amount = models.PositiveIntegerField(_('Entry Quota Amount'), default=1)

    # Periodicity ty of entry
    entry_periodicity = models.CharField(_('Entry Periodicity Type'), choices=Finance.PERIODICITY, default=Finance.MONTHLY, max_length=20)
    
    # Entry Type
    entry_type = models.CharField(_('Entry Type'), choices=Category.ENTRY_TYPE, default=Category.EXPENSE, max_length=20)

    # Relationship between category and launch
    category = models.ForeignKey(Category, verbose_name=_('Entry Category'))

    # User relationship
    entry_user = models.ForeignKey(User, verbose_name=_('User'))

    # Possible values of state value and portion
    OVERDUE = _('Overdue')
    NO_OVERDUE = _('No Overdue Yet')
    ALL_ENTRY = _('All Entry')

    # State of value Enum
    VALUE_STATE = (
        (OVERDUE, _('Overdue')),
        (NO_OVERDUE, _('No Overdue Yet')),
        (ALL_ENTRY, _('All Entry')),
    )

    # State of quota Enum
    QUOTA_STATE = (
        (OVERDUE, _('Overdue')),
        (NO_OVERDUE, _('No Overdue Yet')),
    )

    def __str__(self):

        """This method is responsible for converting to the format string.
        """

        return self.entry_description