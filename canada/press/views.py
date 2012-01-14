from django.shortcuts import get_object_or_404, render
from press.models import Press

def single(request, year, title):
    press = get_object_or_404(Press, date__year=year, title=title)
    context = {
        'press': press
        }
    return render(request, 'press/single.html', context)