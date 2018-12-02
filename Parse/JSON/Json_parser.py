import json as js

file_path = 'FrequentFlyerForum-Profiles.json'

with open(file_path) as f:
    print('Reading!')
    data = js.loads(f.read())
    data = data['Forum Profiles']
    print('End')

#Формирование шапки
headers_list = ['Date',
                'Flight',
                'Codeshare',
                'ArriavalCity',
                'ArriavalPort',
                'ArriavalCountry',
                'DepartureCity',
                'DeparturePort',
                'DepartureCountry',
                'NickName',
                'Passport', # Если нет других TravelDoc
                'Sex',
                'FirstName',
                'LastName',
                'LoyalityProgram',
                'LoyalityStatus',
                'LoyalityNumber'
               ]

flight_headers_list = ['Flight',
                       'Date',
                       'Codeshare',
                       'ArriavalCity',
                       'ArriavalPort',
                       'ArriavalCountry',
                       'DepartureCity',
                       'DeparturePort',
                       'DepartureCountry',
                       'NickName' #Внешний ключ
                       ]

person_headers_list = ['NickName', #Первичный ключ
                       'FirstName',
                       'LastName',
                       'Sex',
                       'Passport'
                       ]
                        
loyality_headers_list = ['LoyalityNumber',
                        'LoyalityProgram',
                        'LoyalityStatus',
                        'NickName' #Внешний ключ
                        ]

#Заголовки
header_string = '' #Общий
flight_header_string = ''
person_header_string = ''
loyality_header_string = ''

def get_header(headers_list):
    header_string = ''
    for word in headers_list:
        header_string += (word +';')
    
    header_string = header_string[:-1]
    return header_string

flight_header_string = get_header(flight_headers_list)
person_header_string = get_header(person_headers_list)
loyality_header_string = get_header(loyality_headers_list)

#Выборка данных по полетам
def get_flights_block(profile_index, flight_index):
    
    flight = data[profile_index]['Registered Flights'][flight_index]
    pers_data = data[profile_index]
    
    flight_block = []

    flight_block.append(flight['Flight'])
    flight_block.append(flight['Date'])
    flight_block.append(str(flight['Codeshare']))
    flight_block.append(flight['Arrival']['City'])
    flight_block.append(flight['Arrival']['Airport'])
    flight_block.append(flight['Arrival']['Country'])
    flight_block.append(flight['Departure']['City'])
    flight_block.append(flight['Departure']['Airport'])
    flight_block.append(flight['Departure']['Country'])
    flight_block.append(pers_data['NickName']) #Внешний ключ

    return flight_block

#Выборка данных по людям
def get_personal_block(profile_index):
    
    pers_data = data[profile_index]
    personal_block = []

    personal_block.append(pers_data['NickName']) #Первичный ключ
    personal_block.append(pers_data['Real Name']['First Name'])
    personal_block.append(pers_data['Real Name']['Last Name'])
    personal_block.append(pers_data['Sex'])
    personal_block.append(pers_data['Travel Documents'][0]['Passports'])

    return personal_block

#Выборка данных по лояльности
def get_loyality_block(profile_index, lprog_index):
    loyality_block = []

    pers_data = data[profile_index]
    
    if len(data[profile_index]['Loyality Programm']) > 0:
        loyalt_data = data[profile_index]['Loyality Programm'][lprog_index]

        loyality_block.append(loyalt_data['Number'][1:])
        loyality_block.append(loyalt_data['programm'])
        loyality_block.append(loyalt_data['Status'])
        loyality_block.append(pers_data['NickName']) #Внешний ключ
        
    return loyality_block #else возвращает пустой массив, учесть в цикле сборки

#### Циклы сборки

#Сборка таблицы полетов
print('Sborka')
flight_res_list = []
for profile_index in range(len(data)):
    for flight_index in range(len(data[profile_index]['Registered Flights'])):
        flight_res_list.append(get_flights_block(profile_index, flight_index))

person_res_list = []
for profile_index in range(len(data)):
    person_res_list.append(get_personal_block(profile_index))
print(person_res_list)

loyality_res_list = []
for profile_index in range(len(data)):
    for lprog_index in range(len(data[profile_index]['Loyality Programm'])):
        loyality_res_list.append(get_loyality_block(profile_index, lprog_index))
print(loyality_res_list)
print('End')
####

# получение массива строк будущего CSV файла
print('ToArr')
def get_csv_lines(res_list):
    csv_lines = []

    for line in range(len(res_list)):
        line_string = ''
        for word in res_list[line]:
            line_string += (str(word) +';')
        line_string = line_string[:-1]
        csv_lines.append(line_string)

    return csv_lines

flight_csv_lines = get_csv_lines(flight_res_list)
fligt_result_csv = [flight_header_string] + flight_csv_lines

person_csv_lines = get_csv_lines(person_res_list)
person_result_csv = [person_header_string] + person_csv_lines

loyality_csv_lines = get_csv_lines(loyality_res_list)
loyality_result_csv = [loyality_header_string] + loyality_csv_lines
print('End')
#вывод в CSV
print('ToCSV')
def to_csv(csv_list, name):
    with open(name + '.csv', 'w') as f:
        for line in csv_list:
            f.write(line + '\n')

to_csv(fligt_result_csv, 'json_fligts_one')
to_csv(person_result_csv, 'json_person_one')
to_csv(loyality_result_csv, 'json_loyality_one')
