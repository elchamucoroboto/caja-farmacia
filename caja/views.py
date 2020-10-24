from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Operacion
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):

    today = date.today()
    operations = Operacion.objects.filter(fecha__year=today.year, fecha__month=today.month, fecha__day=today.day)

    listZelle = [0]
    listPunto = [0]
    listEfectivoD = [0]
    listEfectivoBS = [0]
    fondoCajaD = 0.00
    fondoCajaBs = 0.00
    sumZelle = 0.00
    sumPunto = 0.00
    sumEfectivoD = 0.00
    sumEfectivoBS = 0.00

    def currencyFormat(monto):
        currency = "{:,.2f}".format(monto)
        return currency

    for op in operations:
        if 'ZELLE' in op.metodo.upper():
            listZelle.insert(0, op.monto)
            sumZelle = sum(listZelle)
            

        if 'PUNTO' in op.metodo.upper():
            listPunto.insert(0, op.monto)
            sumPunto = sum(listPunto)

        if 'DOLARES EFECTIVO' in op.metodo.upper():
            listEfectivoD.insert(0, op.monto)
            sumEfectivoD = sum(listEfectivoD)
            

        if 'BOLIVARES EFECTIVO' in op.metodo.upper():
            listEfectivoBS.insert(0, op.monto)
            sumEfectivoBS = sum(listEfectivoBS)

        if 'FONDO DE CAJA DOLARES' in op.metodo.upper():
            fondoCajaD = op.monto

        if 'FONDO DE CAJA BOLIVARES' in op.metodo.upper():
            fondoCajaBs = op.monto

        venta_total_dolares = sumZelle + sumEfectivoD
        venta_total_bolivares = sumPunto + sumEfectivoBS


    template = loader.get_template('caja/index.html')
    context = {
        'operations': operations,
        'sumZelle' : currencyFormat(sumZelle), 
        'sumPunto' : currencyFormat(sumPunto), 
        'sumEfectivoBS' : currencyFormat(sumEfectivoBS) , 
        'venta_total_dolares' : currencyFormat(venta_total_dolares), 
        'venta_total_bolivares' : currencyFormat(venta_total_bolivares), 
        'sumEfectivoD' : currencyFormat(sumEfectivoD), 
        'fondoCajaD' : currencyFormat(fondoCajaD), 
        'fondoCajaBs' : currencyFormat(fondoCajaBs),
    }
    return HttpResponse(template.render(context, request))
