import api.models as models
import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def show(request, refill_id):
    refill = get_object_or_404(models.Refill, pk=refill_id)
    total = models.Refill.objects.filter(growler=refill.growler).count()
    return render(request, 'refill.html', {'refill': refill, 'total': total, 'prize': refill.prize.name})


def index(request):
    shelters = [{'id': s.id, 'name': s.name} for s in models.Shelter.objects.all()]
    beers = [{'id': b.id, 'name': b.name} for b in models.Beer.objects.all()]
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
        refill.prize = random.choice(models.Prize.objects.all())
        refill.location = models.Shelter.objects.get(pk=request.POST['shelter'])
        refill.beer = models.Beer.objects.get(pk=request.POST['beer'])
        refill.save()
        return HttpResponseRedirect(reverse('refill_show', args=(refill.id,)))
