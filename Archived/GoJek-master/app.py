import csv  
import json  
 
print('Start Read CSV')
 
f = open( 'driver_registration.csv', 'r' )  
reader = csv.DictReader( f, fieldnames = ('id', 'date_created', 'date_last_modified','active_date','name','phone','resign_date'
                                          ,'resign_reason','status','tipe','area','operator_id','modified_by','vehicle_type'
                                          ,'helmet_qty','jacket_qty','vehicle_brand','vehicle_year','bike_type'
                                          ,'first_ride_bonus_awarded','is_doc_completed'))  

out = json.dumps( [ row for row in reader ] )  

jsonArray = json.loads(out)

print('Start Wite json')

with open ('export_from_docker.json', 'w') as f :
	for jsonData in jsonArray :
		f.write(str(jsonData) + '\n')

print('Done')