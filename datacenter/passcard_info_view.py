from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render

def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits_by_passcard = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []
    for visit in visits_by_passcard:
        is_strange = visit.is_visit_long()
        visit_duration = visit.format_duration(visit.duration, "%H:%M")
        this_passcard_visit = {"entered_at": visit.entered_at, \
                               "duration": visit_duration, \
                               "is_strange": is_strange}
        this_passcard_visits.append(this_passcard_visit)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
