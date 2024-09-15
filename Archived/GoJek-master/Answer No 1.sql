with 

--1. Reformat order_time into Jakarta Timezone and trunct the time
--2. Distinct the data by fields order date, customer_no and order_type, 
--   the purpose is to see how many order_type that a customer use in one order_date regardless he order_payment
--3. filter order_status = 'Completed'
distdata as (
select distinct DATE(order_time, "Asia/Jakarta") order_date,  
customer_no,
order_type
from `bi-dwhdev-01.source.daily_order` 
where order_status = 'Completed'
order by 1,2,3)

-- Select count of customer for each order_type in a order_date
-- in this query, we know how many order_type a customer us in a day
, cust as (
select order_date, customer_no, count(*) cnt from  distdata
group by order_date, customer_no)

-- Only change the order_time into order_date and use Jakarta timezone
, thedata as (
select DATE(order_time, "Asia/Jakarta") order_date,  
customer_no, 
order_type,
order_payment
from `bi-dwhdev-01.source.daily_order` 
where order_status = 'Completed'
order by 1,2,3)

-- Query to show aggregate data of customer, in this query we can see what order_types are each customer use
-- and what are the order payment
,pre_data as(
select thedata.order_date, 
thedata.customer_no,  
count(thedata.customer_no)cnt_cust,
cust.cnt,
FORMAT("%T", ARRAY_AGG(distinct(thedata.order_type) order by (thedata.order_type)) ) order_type,
FORMAT("%T", ARRAY_AGG(distinct(thedata.order_payment) order by (thedata.order_payment)) )  order_payment
from thedata
inner join cust 
on thedata.order_date = cust.order_date
and thedata.customer_no = cust.customer_no 
group by thedata.order_date, thedata.customer_no, cust.cnt
order by 1,2)

-- aggregate the data
,data_sum as (
select order_date, 
no_of_service, 
sum(total_customer_per_order_type) over (partition by order_date, no_of_service) total_customer,  
order_type,
total_customer_per_order_type,
order_payment
from (
select
order_date, 
cnt as no_of_service, 
replace(replace(replace(order_type,'[',''),']',''),'"','')order_type, 
sum(cnt_cust) total_customer_per_order_type,
replace(replace(replace(order_payment,'[',''),']',''),'"','') order_payment
from pre_data 
group by order_date, cnt, order_type, order_payment
)
order by 1,2,4)

select 
order_date, 
no_of_service, 
total_customer, 
order_type, 
total_customer_per_order_type, 
order_payment  from data_sum

