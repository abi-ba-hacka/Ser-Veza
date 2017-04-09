import api.models as models
import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def show(request, refill_id):
    refill = get_object_or_404(models.Refill, pk=refill_id)
    return render(request, 'refill.html', {'refill': refill, 'prize': refill.get_prize_display()})


def index(request):
    shelters = [{'id': s.id, 'name': s.name} for s in models.Shelter.objects.all()]
    beers = [{'id': b[0], 'name': b[1]} for b in models.Refill.BEER_CHOICES]
    if request.method == 'GET':
        return render(request, 'add_refill.html', {'beers': beers, 'shelters': shelters})
    try:
        code = request.POST['code']
        growler = models.Growler.objects.get(code=code)
    except Exception:
        return render(request, 'add_refill.html', {
            'err': "ID %s invalido." % (code or ''),
            'beers': beers,
            'shelters': shelters,
        })
    else:
        refill = models.Refill()
        refill.growler = growler
        refill.prize = random.choice(models.Refill.PRIZE_CHOICES)[0]
        refill.location = models.Shelter.objects.get(pk=request.POST['shelter'])
        refill.beer = int(request.POST['beer'])
        refill.save()
        return HttpResponseRedirect(reverse('refill_show', args=(refill.id,)))
