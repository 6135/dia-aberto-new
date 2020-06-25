from django.test import TestCase
from configuracao.forms import *
from configuracao.models import *
from configuracao.tests.test_models import create_campus, create_edificio


class TestForms(TestCase):

    def setUp(self):
        self.campus = create_campus()
        self.edificio = create_edificio(self.campus)
        
    def tearDown(self):
        self.edificio.delete()
        self.campus.delete()


    def test_TemaForm(self):
        form = TemaForm(data={
            'tema': 'Informatica'
        })

        self.assertTrue(form.is_valid())

        #invalid

        form = TemaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

    def test_EdificioForm(self):
        
        formEdificio = EdificioForm(data={
            'nome': 'C1',
            'campus': self.campus,
            'image': 'bruv.png'
        })

        self.assertTrue(formEdificio.is_valid())

        #invalid

        formEdificio = EdificioForm(data={
            'nome': 'C1',
            'campus': self.campus.nome,
            'image': 'bruv.png'
        })

        self.assertEquals(len(formEdificio.errors),1)
        formEdificio = EdificioForm(data={})
        self.assertEquals(len(formEdificio.errors),2)

    def test_EspacoForm(self):
        edificio = self.edificio

        form = EspacoForm(data={
            'nome': '2.13',
            'andar': '1',
            'descricao': 'Sala',
            'edificio': edificio
        })
        
        self.assertTrue(form.is_valid())

        #invalid

        form = EspacoForm(data={
            'nome': '2.13',
            'andar': '1',
            'descricao': 'Sala',
            'edificio': None
        })
        self.assertEquals(len(form.errors),1)
        

