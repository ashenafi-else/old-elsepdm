from django.db import models
from elsepublic.models import (
    Base,
    DamAssetInfo,
)
from treebeard.mp_tree import MP_Node
from django.contrib.postgres.fields import (
    JSONField,
    ArrayField,
)


class Brand(Base):
    name = models.CharField(max_length=120)
    brand_external_id = models.CharField(unique=True, max_length=64)

    def __str__(self):
        return f'{self.name}({self.uuid})'


class Collection(Base):
    name = models.CharField(max_length=120)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='collections',
    )


class Material(Base):
    name = models.CharField(max_length=64)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=64)
    available_colors = models.ForeignKey(
        'elsecmh.Color',
        on_delete=models.SET_NULL,
        null=True,
    )

class ProductHierarchy(MP_Node, Base):
    name = models.CharField(max_length=64)
    node_order_by = ['name', ]


class ShoePairSettings(Base):

    AXIS_XYZ = 'xyz'
    AXIS_XZY = 'xzy'
    AXIS_YXZ = 'yxz'
    AXIS_YZX = 'yzx'
    AXIS_ZXY = 'zxy'
    AXIS_ZYX = 'zyx'

    AXES = (
        (AXIS_XYZ, 'XYZ'),
        (AXIS_XZY, 'XZY'),
        (AXIS_YXZ, 'YXZ'),
        (AXIS_YZX, 'YZX'),
        (AXIS_ZXY, 'ZXY'),
        (AXIS_ZYX, 'ZYX'),
    )
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    axes = models.CharField(max_length=3, choices=AXES)
    distance = models.FloatField(verbose_name='Distance between models')
    shouldnt_be_reflected = ArrayField(
        models.CharField(max_length=200),
        default=list,
        verbose_name='Objects that should not be reflected',
    )

    def __str__(self):
        return self.name


class Product(Base):
    DEFAULT_STATE = 'empty'

    STATES = (
        (DEFAULT_STATE, 'Empty'),
    )
    state = models.CharField(
        max_length=64,
        choices=STATES,
        default=DEFAULT_STATE,
    )
    name = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
    activity_log = models.TextField(null=True)
    description = models.TextField(null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    product_hierarchy = models.ForeignKey(
        ProductHierarchy, on_delete=models.CASCADE)
    active_revision = models.ForeignKey(
        'ProductRevision',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )
    previous_revision = models.ForeignKey(
        'ProductRevision',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )


class ProductRevision(Base):
    NEW = 'new'
    UPDATED = 'updated'
    PARSED = 'parsed'
    READY = 'ready'
    PUBLISHING = 'publishing'
    PUBLISHED = 'published'

    STATES = (
        (NEW, 'New'),
        (UPDATED, 'Updated'),
        (PARSED, 'Parsed'),
        (READY, 'Ready'),
        (PUBLISHING, 'Publishing'),
        (PUBLISHED, 'Published'),
    )

    product = models.ForeignKey(
        'Product',
        related_name='revisions',
        on_delete=models.CASCADE)
    state = models.CharField(max_length=64, choices=STATES, default=NEW)
    json_configuration = JSONField(null=True)

    @property
    def version(self):
        return self.product.revisions.count()

    class Meta:
        ordering = ('-created', )


class ProductComponent(Base):
    product = models.ForeignKey(
        ProductRevision,
        related_name='product_components',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default='')
    component = models.CharField(max_length=64)
    configurable = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    optional = models.BooleanField(default=False)
    order = models.IntegerField()


class ProductStructure(Base):
    EXPORT_NAME_TEMPLATE = 'prod_{}_comp_{}_{}'

    component = models.ForeignKey(
        ProductComponent,
        related_name='product_structures',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default='')
    export_name = models.CharField(max_length=255)
    structure = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.export_name = self.EXPORT_NAME_TEMPLATE.format(
            self.component.product.product.name,
            self.component.component,
            self.structure,
        )
        super(ProductStructure, self).save(*args, **kwargs)

    def __str__(self):
        return self.export_name


class ProductElement(Base):
    structure = models.ForeignKey(
        ProductStructure,
        related_name='product_elements',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default='')
    element = models.CharField(max_length=64)
    configurable = models.BooleanField(default=True)
    path = models.CharField(max_length=64)
    active_material = models.CharField(max_length=64)
    active_color = models.CharField(max_length=64, null=True)
    materials = ArrayField(models.CharField(max_length=200), default=list)


class Configuration(Base):
    CREATED = 'created'
    RENDERED = 'rendered'
    PUBLISHED = 'published'

    STATES = (
        (CREATED, 'Created'),
        (RENDERED, 'Rendered'),
        (PUBLISHED, 'Published'),
    )
    state = models.CharField(max_length=64, choices=STATES, default=CREATED)
    product_revision = models.ForeignKey(
        ProductRevision, on_delete=models.CASCADE)


class ConfigurationElement(Base):
    element = models.ForeignKey(ProductElement, on_delete=models.CASCADE)
    configuration = models.ForeignKey(
        Configuration,
        on_delete=models.CASCADE,
        related_name='configuration_elements')
    material = models.CharField(max_length=64)
    color = models.CharField(max_length=64)


class ProductTour(Base):
    product = models.ForeignKey(ProductRevision, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    camera = models.CharField(max_length=64)
    resolution_x = models.PositiveIntegerField()
    resolution_y = models.PositiveIntegerField()
    frames = models.PositiveIntegerField()
    circles = models.PositiveIntegerField()
    frame_rate = models.PositiveIntegerField()
    filename = models.CharField(max_length=64)
    extended_json = JSONField()


def generate_file_name(self, filename):
    """ Generates file name for assets """
    return "elsepdm/{}/{}".format(self.uuid, filename)


class PdmAsset(Base, DamAssetInfo):
    MODEL_ASSET = 'MODEL_ASSET'
    PREVIEW_ASSET = 'PREVIEW_ASSET'
    B4W_ASSET = 'B4W_ASSET'
    TOUR_GIF_ASSET = 'TOUR_GIF_ASSET'
    FRAMES_ASSET = 'FRAMES_ASSET'
    OBJ_ASSET = 'OBJ_ASSET'
    RESOURCE_ASSET = 'BLEND_RESOURCE'
    PAIR_ASSET = 'PAIR_ASSET'

    ASSET_TYPES = (
        (MODEL_ASSET, 'Model asset'),
        (PREVIEW_ASSET, 'Preview asset'),
        (B4W_ASSET, 'B4W asset'),
        (TOUR_GIF_ASSET, 'Tour gif asset'),
        (FRAMES_ASSET, 'Frames asset'),
        (OBJ_ASSET, 'Obj asset'),
        (RESOURCE_ASSET, 'Resource asset'),
        (PAIR_ASSET, 'Pair asset'),
    )

    asset_type = models.CharField(max_length=255, choices=ASSET_TYPES)

    class Meta:
        abstract = True


class ComponentAsset(PdmAsset):
    structure = models.ForeignKey(
        'ProductStructure',
        on_delete=models.CASCADE,
        related_name='assets',
    )


class ProductAsset(PdmAsset):
    configuration = models.ForeignKey(
        'Configuration',
        on_delete=models.CASCADE,
        related_name='assets',
    )


class ResourceAsset(PdmAsset):
    TYPE_ENVIRONMENT = 'ENV'
    TYPE_SETTINGS = 'SETTINGS'
    TYPE_BACKGROUND = 'BACKGROUND'

    RESOURCE_TYPES = (
        (TYPE_ENVIRONMENT, 'Environment'),
        (TYPE_SETTINGS, 'Settings'),
        (TYPE_BACKGROUND, 'Background'),
    )

    type = models.CharField(
        max_length=255,
        choices=RESOURCE_TYPES,
    )
    name = models.CharField(max_length=255)
    pdm_brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='resource_assets',
    )
