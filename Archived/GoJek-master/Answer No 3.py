import csv  
import json  
  
f = open( 'driver_registration.csv', 'r' )  
reader = csv.DictReader( f, fieldnames = ('id', 'date_created', 'date_last_modified','active_date','name','phone','resign_date'
                                          ,'resign_reason','status','tipe','area','operator_id','modified_by','vehicle_type'
                                          ,'helmet_qty','jacket_qty','vehicle_brand','vehicle_year','bike_type'
                                          ,'first_ride_bonus_awarded','is_doc_completed'))  

out = json.dumps( [ row for row in reader ] )  

jsonArray = json.loads(out)

with open("Question3.json", 'w') as f:
    for jsonArrays in jsonArray :
        f.write(str(jsonArrays)+ '\n')