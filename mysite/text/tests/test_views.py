from django.test import TestCase
from django.urls import reverse
from text.models import Cases, SRQs

class LoanedBookInstancesByUserListViewTest(TestCase):


    def test_uses_correct_template(self):
            resp = self.client.get(reverse('test', kwargs={}) )
            self.assertEqual( resp.status_code,200)

            #Check we used correct template
            self.assertTemplateUsed(resp, 'model_classification.html')