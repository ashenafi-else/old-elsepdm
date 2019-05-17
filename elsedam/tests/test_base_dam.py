import os
from django.test import TestCase

from elsedam.services import AzureService
from elsedam.models import Brand


class TestBaseDam(TestCase):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    fixtures = (fixtures_models_path,)

    def setUp(self):
        self.default_brand = Brand.objects.filter(brand_external_id='1').first()
        self.brand = Brand.objects.filter(uuid="642bbbe6-d21b-11e8-a8d5-f2801f1b9fd1").first()
        self.mock_object = AzureService
