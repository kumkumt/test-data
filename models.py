import logging

from django.db import models
from django.db.models import Q

from tienda.core.models import BaseModel
from tienda.product_selection.types import (
    DEFAULT_EXPIRATION_HANDLING_STRATEGY,
    DEFAULT_PROMISED_EXPIRATION_DAYS_FOR_SALE,
    ExpirationHandlingStrategy,
)
from tienda.products.types import ProductStatus

from .managers import ProductRegionStatusQuerySet, SeasonQuerySet

logger = logging.getLogger(__name__)

ProductRegionStatusManager = models.Manager.from_queryset(ProductRegionStatusQuerySet)


class ProductRegionStatus(BaseModel):
    """
    A representation of Product status inside a Region.
    """

    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="region_statuses"
    )

    region = models.ForeignKey(
        "core.Region", on_delete=models.CASCADE, related_name="product_statuses"
    )

    product_status = models.SmallIntegerField(choices=ProductStatus.choices)

    # Max allowed quantity to purchase in a single purchase (can be extended to
    # look at per day/week/months as well)
    consumer_quantity_limit = models.PositiveIntegerField(
        "consumer quantity limit",
        blank=True,
        null=True,
        help_text="Max allowed quantity in a consumer purchase",
    )
    organization_quantity_limit = models.PositiveIntegerField(
        "organization quantity limit",
        blank=True,
        null=True,
        help_text="Max allowed quantity in a organization purchase",
    )

    # Availability
    available_for_consumers = models.BooleanField(
        "available for consumers",
        default=True,
        help_text="Makes the product available for consumers (and anonymous users).",
    )
    available_for_organizations = models.BooleanField(
        "available for organizations",
        default=True,
        help_text="Makes the product available for organizations.",
    )

    published_time = models.DateTimeField(
        "published time",
        null=True,
        blank=True,
        help_text="Used for sorting the latest additions to the store.",
    )

    season = models.ForeignKey(
        "product_selection.Season",
        verbose_name="season",
        blank=True,
        null=True,
        help_text="Set if the product should only be available in the specified season",
        on_delete=models.SET_NULL,
    )

    # The date of first planned picking of the product
    # Purchasing algorithm generally attempts to have the product ready in the shelves by this date.
    introduction_date = models.DateField(
        "introduction date",
        blank=True,
        null=True,
        help_text="First planned fulfillment date",
    )

    # The date of last planned picking of the product
    # Purchasing will ramp down to this date, but the product will still be sold until the inventory is empty.
    termination_date = models.DateField(
        "termination date",
        blank=True,
        null=True,
        help_text="Last planned fulfillment date",
    )

    # Reference product. Used in purchasing to improve forecast accuracy on new products.
    reference_product = models.ForeignKey(
        "products.Product",
        verbose_name="reference product",
        blank=True,
        null=True,
        related_name="referenced_by_product_set",
        help_text="Set to the most similar product (use frontend ID). Used to improve purchasing of "
        "new products until sufficient sales history is available.",
        on_delete=models.SET_NULL,
    )

    reference_scaling_factor = models.DecimalField(
        "reference scaling factor",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="A factor used to scale this product sales compared to the reference product. "
        "Ex. 0.2 for if you assume that this product will sell 20 % compared to the reference product.",
    )

    promised_expiration_days_for_sale = models.PositiveIntegerField(
        "promised expiration days for sale",
        default=DEFAULT_PROMISED_EXPIRATION_DAYS_FOR_SALE,
        help_text="The promised number of expiration days for sale to customers.",
    )

    expiration_handling = models.IntegerField(
        "expiration handling",
        choices=ExpirationHandlingStrategy.choices,
        default=DEFAULT_EXPIRATION_HANDLING_STRATEGY,
    )

    objects = ProductRegionStatusManager()

    class Meta:
        verbose_name = "product region status"
        verbose_name_plural = "product region statuses"
        unique_together = (("product", "region"),)
        constraints = [
            # Ensure that products available for sale have published time set
            models.CheckConstraint(
                check=(
                    Q(
                        published_time__isnull=False,
                        product_status=ProductStatus.FOR_SALE,
                    )
                    | ~Q(product_status=ProductStatus.FOR_SALE)
                ),
                name="%(app_label)s_%(class)s_published_time_set",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product} status in {self.region}: {self.get_product_status_display()}"

    def is_for_sale(self) -> bool:
        return self.product_status == ProductStatus.FOR_SALE

    def is_discontinued(self) -> bool:
        return self.product_status in [
            ProductStatus.DISCONTINUED,
            ProductStatus.DISCARDED_DRAFT,
        ]

    def get_audit_logs(self):

        from tienda.audit_logs.models import LogEntry

        return LogEntry.objects.get_for_object(self).order_by("-created_time")[:5]


SeasonManager = models.Manager.from_queryset(SeasonQuerySet)


class Season(models.Model):
    """
    Groups products that are only available within a specific, time-limited period (e.g. Christmas).
    """

    # Identifies the season, e.g. "Christmas"
    name = models.CharField(
        "name", max_length=100, help_text='Descriptive name, like "Christmas"'
    )

    start_date = models.DateField("start date", help_text="First date of the season")
    end_date = models.DateField("end date", help_text="Last date of the season")

    objects = SeasonManager()

    class Meta:
        db_table = "backend_products_season"
        verbose_name = "season"
        verbose_name_plural = "seasons"

    def __str__(self):
        return self.name

   
class ExpiryHandling (models.Model):
    c_productid = models.BigIntegerField("c_productid" , default=0)
    s_productid = models.BigIntegerField("s_productid",default=0)
    for_supplier = models.PositiveIntegerField ("for_supplier",default=0)
    for_sale = models.PositiveIntegerField ("for_sale",default=0)
    exp_handling = models.CharField("exp_handling",max_length=10,default="normal")
    objects = models.Manager()
   

    class Meta:
        db_table = "expiry_handling"
        verbose_name= "expiry"
        verbose_name_plural="expirys"
        
    #def __str__(self):
    #   return self
    
    def __str__(self) -> str:
            return f"{self.c_productid}" , f"{self.s_productid}" ,f"{self.for_supplier}" ,f"{self.for_sale}",f"{self.exp_handling}"
               
  

  
