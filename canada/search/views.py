from itertools import chain

from django.shortcuts import render
from django.db.models import Q

from artists.models import Artist
from exhibitions.models import Exhibition
from press.models import Press
from updates.models import Update


def form(request):
    errors = []

    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a term.')
        elif len(q) > 20:
            errors.append('Enter less than 20 characters.')
        else:
            results = list(chain(Artist.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q)),
                                 Exhibition.objects.filter(name__icontains=q),
                                 Press.objects.filter(Q(title__icontains=q) | Q(publisher__icontains=q)),
                                 Update.objects.filter(name__icontains=q)
                                ))
            return render(request, 'search/results.html', {'results': results, 'query': q})
    return render(request, 'search/form.html', {'errors:': errors})
