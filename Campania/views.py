from django.shortcuts import render
from .forms import CampanaForm

def crear_campana(request):
    form = CampanaForm()
    return render(request, 'crear_campana.html', {'form': form})

