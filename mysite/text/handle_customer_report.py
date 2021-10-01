from .models import Cases, SRQs

SECRET_KEY = 'vc4v*1mu4z%$(c063c^o@0011xw)ridk-zvm)(cby5$&)t7$+&'


def handle_customer_report(case_pandas_dateframe, srq_pandas_dateframe):

    caseNumberindb = Cases.objects.values('CaseNumber')
    caseNumberindb_list = []
    objs = []

    for i in caseNumberindb:
        caseNumberindb_list.append(i['CaseNumber'])

    for i in range(len(case['CaseNumber'])):
        if case['CaseNumber'][i] not in caseNumberindb_list:
            objs.append(Cases(
                    CaseNumber= case['CaseNumber'][i],
                    CreatedDate= pd.to_datetime(case['CreatedDate'][i]),
                    Model= (str(case['Model'][i]).upper()),
                    SerialNumber= str(case['SerialNumber'][i]),
                    Symptom= str(case['Symptom'][i]),
                    Diagnosis= str(case['Diagnosis'][i]),
                    Description= str(case['Description'][i]),
                ))
                        
    newlyCreatedCases = Cases.objects.bulk_create(objs)

    SRNumberindb = SRQs.objects.values('SRNumber')
    SRNumberindb_list = []
    objs = []

    for i in SRNumberindb:
        SRNumberindb_list.append(i['SRNumber'])

    for i in range(len(srq['SRNumber'])):
        if srq['SRNumber'][i] not in SRNumberindb_list:
            objs.append(SRQs(
                        SRNumber= srq['SRNumber'][i],
                        SRType= str(srq['SRType'][i]),
                        CreatedDate= pd.to_datetime(srq['CreatedDate'][i]),
                        Model= (str(srq['Model'][i]).upper()),
                        SerialNumber= str(srq['SerialNumber'][i]),
                        ErrorCode= str(srq['ErrorCode'][i]),
                        InternalNotes= str(srq['InternalNotes'][i]),
            ))

    newlyCreatedCases = SRQs.objects.bulk_create(objs)
                    