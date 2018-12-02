import re

##Match 1
##Group `FromCity`	5-12	`Aalborg`
##Group `FromCountry`	14-24	`DenmarkAAL`
##Group `ToCity`	27-37	`Amsterdam `
##Group `ToCountry`	39-50	`Netherlands`
##Group `ToAirport`	50-53	`AMS`
##Group `Validity`	103-120	`01 Nov  -  31 Jan`
##Group `Days`	120-127	`1234567`
##Group `DepTime`	127-132	`06:00`
##Group `ArrTime`	132-137	`07:25`
##Group `Flight`	137-143	`KL1328`
##Group `Aircraft`	143-146	`73W`
##Group `TravelTime`	146-151	`1H25M`

##Match 2
##Full match	151-199	`01 Nov  -  31 Jan123456712:1013:35KL133473W1H25M`
##Group `Validity`	151-168	`01 Nov  -  31 Jan`
##Group `Days`	168-175	`1234567`
##Group `DepTime`	175-180	`12:10`
##Group `ArrTime`	180-185	`13:35`
##Group `Flight`	185-191	`KL1334`
##Group `Aircraft`	191-194	`73W`
##Group `TravelTime`	194-199	`1H25M`

pattern = r"(FROM:(?P<FromCity>[\w\s\/]*)\s*,\s*(?P<FromCountry>[\w\s\/]*)TO:(?P<ToCity>[\w\s\/]*)\s*,\s*(?P<ToCountry>[\w\s\/]*)(?P<ToAirport>[A-Z]{3})ValidityDaysDepTimeArrTimeFlightAircraftTravelTime)*(?P<Validity>\d\d\s\w{3}\s*-\s*\d\d\s\w{3})(?P<Days>[\d\s]*)(?P<DepTime>\d\d:\d\d)(?P<ArrTime>\d\d:\d\d[+1]*)(?P<Flight>[A-Z]{2}\d{3,4})\**(?P<Aircraft>[A-Z\d]{3})(?P<TravelTime>\d{1,2}H\d*M)"
header_string = 'FromCity,FromCountry,ToCity,ToCountry,ToAirport,Validity,Days,DepTime,ArrTime,Flight,Aircraft,TravelTime\n'

with open('text_pdf.txt', 'r') as pdf:
    text = pdf.readlines()
    
    with open('pdf_all.csv', 'w') as file:
        file.write(header_string)
        for page in text:
            splt = re.split(pattern, page)
            if (splt != None and len(splt) > 1): 
                if(splt[1] != None):
                    inpage_cities_string = ''
                    for i in range(2, 7): #City, country, etc. - similar for page
                        inpage_cities_string += (splt[i] + ',')
                    inpage_cities_string = inpage_cities_string[:-1]

                    steps = int((len(splt) - 1) / 14)
                    for step in range(0, steps):
                        res_string = inpage_cities_string
                        for i in range(7 + 14 * step, 14 + 14 * step):
                            res_string += (splt[i] + ',')
                        res_string = res_string[:-1] + '\n'
                        file.write(res_string)

    
