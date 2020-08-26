insert into bangazonapp_product
values
    (null, "Apple Watch", 399, "Portable Laptop", 8, "Murfreesboro, TN", null, "2020-08-24", 2, 1);

insert into bangazonapp_order
values
    (null, "2020-08-25", 1, 2);

insert into bangazonapp_productorder
values
    (null, 2, 2);

insert into bangazonapp_paymenttype
values
    (null, "Wells Fargo", "4737-0218-7567-1687", "2023-08-31", "2020-08-24", 1);


delete from bangazonapp_productorder
where id=2;