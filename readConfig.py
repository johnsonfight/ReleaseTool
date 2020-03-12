import configparser
 
config = configparser.ConfigParser()
config.read('readConfig.ini')
section_a_Value = config.get('Section_A', 'Key_ABC')#GET "Value_ABC"
section_b_Value = config.get('Section_B', 'Alarm') #Get "Some thing here"
print ("section_a_Value = ", section_a_Value )
print ("section_b_Value = ", section_b_Value )