from django.shortcuts import get_object_or_404, render
from press.models import Press

def single(request, year, slug):
    press = get_object_or_404(Press, date__year=year, slug=slug)
    context = {
        'press': press
        }
    return render(request, 'press/single.html', context)
