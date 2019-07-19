from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render

def storage_information_view(request):
    
    unfinished_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []

    for visit in unfinished_visits:
        passcard_of_entered = visit.passcard
        
        visit_duration = visit.format_duration(visit.duration, "%H:%M")
        is_strange = visit.is_visit_long()
        non_close_visit = {"who_entered": passcard_of_entered.owner_name, \
                           "date": visit.entered_at, \
                           "duration": visit_duration, \
                           "is_strange": is_strange}
        non_closed_visits.append(non_close_visit)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
