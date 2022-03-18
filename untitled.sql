select distinct DocNumber, DocDate from Document join Receive on DocID = RecID;

select ProdName, unit, Cost, Count, (Cost*Count) as sum from Products 
join Receive on Receive.ProdID = Products.ProdID where RecID = 1;

select Products.ProdName, Products.unit, Products.Cost from Products;

select ProdName, unit, Cost, sum(Count) as Quantity from Receive 
join Products on Products.ProdID = Receive.ProdID group by Receive.ProdID;

