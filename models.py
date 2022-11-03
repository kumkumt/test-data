import logging

from django.db import models
from django.db.models import Q

   
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
               
  

  
