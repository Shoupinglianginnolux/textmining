from import_export import resources
from .models import Cases, SRQs

class SRQResource(resources.ModelResource):
    class Meta:
        model = SRQs

class CasesResource(resources.ModelResource):
    class Meta:
        model = Cases