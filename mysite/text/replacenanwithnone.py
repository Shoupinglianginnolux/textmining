for i in range(len(messageB['OSRNumber'])):
    OSR.objects.filter(OSRNumber=str(messageB['OSRNumber'][i])).update(
        OverSent_Parts=str(messageB['OverSent_Parts'][i]),
        UnderSent_Parts=str(messageB['UnderSent_Parts'][i]),
        F2score=str(messageB['F2score'][i])
        )

from django.db.models import Q

def get_error_code_from_srq():
    a = OSR.objects.filter(
        Q(ErrorCode='nan') | Q(ErrorCode__isnull=True))
    for i in a:
        if SRQs.objects.filter(SRNumber=str(i.OSRNumber)).count() > 0:
            i.ErrorCode = SRQs.objects.filter(SRNumber=str(i.OSRNumber))[0].ErrorCode
            i.save()