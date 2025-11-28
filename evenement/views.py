from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Evenement, ImageEvenement
from .forms import EvenementForm, ImageEvenementFormSet

def liste_evenements(request):
    """Affiche uniquement les événements validés pour le public"""
    search_query = request.GET.get('search', '')

    # Affiche seulement les événements validés
    evenements = Evenement.objects.filter(statut='valide')

    if search_query:
        evenements = evenements.filter(
            Q(nom__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    context = {
        'evenements': evenements,
        'search_query': search_query,
    }
    return render(request, 'evenement/evenements.html', context)


def ajouter_evenement(request):
    """Créer un nouvel événement (statut en_attente par défaut)"""
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        formset = ImageEvenementFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            evenement = form.save(commit=False)
            evenement.save()

            # Sauvegarde des images
            images = formset.save(commit=False)
            for image in images:
                image.evenement = evenement
                image.save()

            messages.success(
                request, 
                '✅ Événement créé avec succès ! Il sera visible après validation par un administrateur.'
            )
            return redirect('liste_evenements')
    else:
        form = EvenementForm()
        formset = ImageEvenementFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'evenement/ajouter.html', context)


def detail_evenement(request, pk):
    """Affiche les détails d'un événement validé"""
    evenement = get_object_or_404(Evenement, pk=pk, statut='valide')
    context = {'evenement': evenement}
    return render(request, 'evenement/detail.html', context)
