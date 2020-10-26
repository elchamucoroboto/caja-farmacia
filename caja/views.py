from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Operacion
from datetime import date
from django.contrib.auth.decorators import login_required
from .forms import opForm, fechaForm
from django.utils import timezone
import datetime



# Create your views here.
@login_required(login_url='/login')
def index(request):

    from .forms import opForm

    if request.method == 'GET':
        form = opForm
        today = date.today()
        operations = Operacion.objects.filter(fecha__year=today.year, fecha__month=today.month, fecha__day=today.day)
        template = loader.get_template('caja/index.html')

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
        venta_total_dolares = 0.00
        venta_total_bolivares = 0.00

        for op in operations:
            if 'ZELLE' in op.metodo:
                listZelle.append(op.monto)
                sumZelle = sum(listZelle)

        context = {'operations': operations,
                    'form': form,
                    'sumZelle': sumZelle}
        template = loader.get_template('caja/index.html')
        return HttpResponse(template.render(context, request))
    
    else:

        form = opForm(request.POST)
        if form.is_valid():

            monto = form.cleaned_data['monto']
            metodo = form.cleaned_data['metodo']
            motivo = form.cleaned_data['motivo']
            op = Operacion(monto=monto, metodo=metodo,motivo=motivo,fecha=timezone.now()) #fecha=date.today()
            op.save()

        return HttpResponseRedirect('/')



def informes(request):
    
    if request.method == 'POST':
        form = fechaForm(request.POST)
        if form.is_valid():

            desde = form.cleaned_data['desde'] 
            hasta = form.cleaned_data['hasta']

            #desde = str(desde)
            #desde = desde.replace('-', ',')
            #hasta = str(hasta)
            #hasta = hasta.replace('-', ',')

            o = Operacion.objects.filter(fecha__date__range=[desde, hasta])

            

            

            context = {'desde': desde,
                    'hasta': hasta}
            return HttpResponse(str(o[1].monto))

    else:
    
        form = fechaForm
    
        template = loader.get_template('caja/informes.html')
        context = {'form': form }
        return HttpResponse(template.render(context, request))


'''
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
        venta_total_dolares = 0.00
        venta_total_bolivares = 0.00

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
        '''