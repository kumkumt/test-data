SELECT sp.price_trade_item_id ,sp.trade_item_id
from public.suppliers_supplierproduct as sp
 where sp.price_trade_item_id in
 (
select c_productid
FROM public.expiry_handling  as eh )
or 
sp.trade_item_id in
(select s_productid
FROM public.expiry_handling  as eh)
	
	
	

	
	
