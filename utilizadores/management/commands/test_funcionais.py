import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from utilizadores.models import Administrador
from django.core.management import call_command
from dia_aberto.utils import init_driver


class Command(BaseCommand):
    help = 'Corre testes funcionais. Exemplo: manage.py test_funcionais firefox [--test inscricoes] [--custom]'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str,
                            help='Especifica a app a testar')
        parser.add_argument('browser', type=str,
                            help='O browser no qual correr os testes')

        # Optional argument
        parser.add_argument('-c', '--custom', action='store_true',
                            help='Utiliza o driver que estiver na PATH')
        parser.add_argument('-k', '--keepdb', action='store_true',
                            help='Manter a db')

    def handle(self, *args, **options):
        browser = options['browser']
        app = options['app']
        custom = options['custom']
        keepdb = options['keepdb']

        if custom:
            init_driver(browser, use_custom_driver=True)
        else:
            init_driver(browser)

        _args = []
        if keepdb:
            _args.append('--keepdb')

        call_command(
            'test', f'{app}/tests/funcionais', *_args)
