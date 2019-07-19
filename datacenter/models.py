from django.utils import timezone
from django.db import models
from string import Template


class DurationTemplate(Template):
    delimiter = "%"   


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
    
    def get_duration(self):
        """Count duration of visit and return timedelta
        
        Duration of visit equal difference between leaved_at and entered_at. If visit haven't leaved_at, function get now time instead leaved_at
        
        :return: give timedelta
        :rtype: timedelta

        """
        now = timezone.now() #+ timezone.timedelta(hours=3)
        if self.leaved_at:
            return self.leaved_at - self.entered_at
        return now - self.entered_at

    def is_visit_long(self, minutes=60):
        """The function checks being visit long. 
        
        The visit is long if it takes more than :param minutes. 

        :param mintes: set the limit for normal visit
        :type: int
        :return: give True if visit is long, otherwise give False
        :rtype: bool

        """
        visit_duration = self.get_duration()
        if visit_duration > timezone.timedelta(minutes=minutes): 
            return True
        return False
    
    duration = property(get_duration)

    def format_duration(self, duration, frmt):
        """ Convert duration of visit from timedelta to string in need format
        
        String format(examples):
        %D days %H:%M:%S duration like str of timedelta 
        %H:%M - duration in hours and minutes
        %D - duration in days
        
        :param duration: duration of visit
        :type: timedelta
        :param frmt: set string format fo duration
        :type: string

        :return: give duration on 
        :rtype: string

        """
        residual = 0
        d = {}
        if "%D" in frmt:
            d["D"] = duration.days
        else:
            residual = duration.days*24*3600 
            residual += duration.seconds
        if "%H" in frmt:     
            d["H"], residual = divmod(residual, 3600)
            if  d["H"] in range(10):
              d["H"]= "0" + str(d["H"])
        if "%M" in frmt:
            d["M"], residual = divmod(residual, 60)
            if  d["M"] in range(10):
                d["M"]= "0" + str(d["M"])
        d["S"] = residual
        if  d["S"] in range(10):
            d["S"]= "0" + str(d["S"])
        template = DurationTemplate(frmt)
        return template.substitute(**d)
