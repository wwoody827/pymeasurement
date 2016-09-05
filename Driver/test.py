import visa
rm = visa.ResourceManager()
print(rm.list_resources())


keithley = rm.open_resource("GPIB::21")
keithley.write("*rst; status:preset; *cls")

keithley.write(":SOUR:VOLT 10")