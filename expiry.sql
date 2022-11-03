
select ep.* ,ti.gtin
from
public.product_selection_productregionstatus prg
join public.products_product pr
on prg.product_id=pr.id
join public.trade_items_tradeitem ti
on ti.product_id=pr.id 
join suppliers_supplierproduct sp
on sp.price_trade_item_id= ti.id
join public.expiry_handling ep
on ep.c_productid::int8= ti.gtin::int8



select ep.*
from public.trade_items_tradeitem ti ,
public.expiry_handling ep
where  (ti.gtin::int8)= ep.c_productid::int8
or  (ti.gtin::int8)= ep.s_productid::int8




