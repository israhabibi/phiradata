import argparse
from datetime import datetime, timedelta
from google.cloud import bigquery
client = bigquery.Client()

today = datetime.now().strftime('%Y-%m-%d')
yestday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store', dest='start_date', default=today, nargs='?')
parser.add_argument('-e', action='store', dest='end_date', default=yestday, nargs='?')

args = parser.parse_args()

if args.start_date == today:
    h = today
    h_1 = yestday
    print(h, h_1)
else:
    h = args.start_date
    h_1 = args.end_date
    print(h, h_1)

# query utama
query = """
    with 

--1. Reformat order_time into Jakarta Timezone and trunct the time
--2. Distinct the data by fields order date, customer_no and order_type, 
--   the purpose is to see how many order_type that a customer use in one order_date regardless he order_payment
--3. filter order_status = 'Completed'
distdata as (
select distinct DATE(order_time, "Asia/Jakarta") order_date,  
customer_no,
order_type
from `root-patrol-237412.order.daily_ordr` 
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
from `root-patrol-237412.order.daily_ordr` 
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
--distinct order_date
order_date, 
no_of_service, 
total_customer, 
order_type, 
total_customer_per_order_type, 
order_payment  
from data_sum
where order_date <= @h and order_date >= @h_1
;
"""
query_params = [
    bigquery.ScalarQueryParameter("h", "STRING", h),
    bigquery.ScalarQueryParameter("h_1", "STRING", h_1),
]
job_config = bigquery.QueryJobConfig()
job_config.query_parameters = query_params
query_job = client.query(
    query,
    # Location must match that of the dataset(s) referenced in the query.
    location="US",
    job_config=job_config,
)  # API request - starts the query

thedata = []
# Print the results
for row in query_job:
    # print("{}: \t{}".format(row.order_date, row.no_of_service, row.total_customer, 
    #     row.order_type, row.total_customer_per_order_type, row.order_payment))
    # print(row.order_date, row.no_of_service, row.total_customer, 
    #      row.order_type, row.total_customer_per_order_type, row.order_payment)
    thedata.append((row.order_date, row.no_of_service, row.total_customer, 
         row.order_type, row.total_customer_per_order_type, row.order_payment))

with open("Question2.json", 'w') as f:
    for data in thedata :
        f.write(str(data)+ '\n')

assert query_job.state == "DONE"