from django import forms
#from .choices import METODO_CHOICES

class opForm(forms.Form):
    monto = forms.FloatField(required=True)
    #c =
    metodo = forms.ChoiceField(choices=[("1", "PUNTO DE VENTA"), ("2", "BOLIVARES EN EFECTIVO"),("3", "DOLARES EN EFECTIVO"),("4", "ZELLE"),("5", "FONDO CAJA BOLIVARES"),("4", "FONDO CAJA DOLARES")], required=True)
    motivo = forms.CharField(required=True)

