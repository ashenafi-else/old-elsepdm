import os
from django.test import TestCase
from elsepdm.models import (
    ProductHierarchy,
    Brand,
    Collection,
)


class TestBasePdm(TestCase):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')

    def setUp(self):
        self.root = ProductHierarchy.add_root(name='test_product_hierarchy')
        self.brand = Brand.objects.create(brand_external_id='test_brand_id')
        self.collection = Collection.objects.create(name='test collection', brand=self.brand)
        self.fake_uuid = "111111d2-d3ec-4444-5555-6d77df8a99aa"
