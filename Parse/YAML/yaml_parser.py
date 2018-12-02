import yaml

print("Here we go!")

data = yaml.load(open("SkyTeam-Exchange1217.yaml"))

print("Выборка по программе лояльности")

#Выборка по программе лояльности
def get_fare_programm(flight_date_key,flight_number_key,ff_key):
    ff = data[flight_date_key][flight_number_key]['FF']
    
    ff_list = []
    ff_list.append(flight_date_key)
    ff_list.append(flight_number_key)
    ff_list.append(ff_key.split()[0])
    ff_list.append(ff_key.split()[1])
    ff_list.append(ff[ff_key]['CLASS'])
    ff_list.append(ff[ff_key]['FARE'])
    ff_list.append(data[flight_date_key][flight_number_key]['FROM'])
    ff_list.append(data[flight_date_key][flight_number_key]['TO'])
    return ff_list

fare_final_list = []
print("Сборка программы лояльности")
#Цикл сбора данных по программам лояльности
for k1 in data.keys():
    for k2 in data[k1].keys():
        for k3 in data[k1][k2]["FF"].keys():
            fare_final_list.append(get_fare_programm(k1,k2,k3))

print("Преобразование в строку")
#Преобразование в строку
def get_csv_line(final_list):
    csv_line=[]
    for flight in range(len(final_list)):
        line=''
        for element in final_list[flight]:
            line+=(element+';')
        line=line[:-1]
        csv_line.append(line)
    return csv_line

fare_csv_list = get_csv_line(fare_final_list)
print("Запись в csv")
#Запись в csv
def write_to_csv(csv_lines_list, file_name):
    with open(file_name + '.csv', 'a') as f:
        for line in csv_lines_list:
            f.write(line + '\n')
            
#Преобразование заголовков в строку
def headers_assemble(headers_list):
    line=""
    for element in headers_list:
        line += (element +';')    
    line = line[:-1]
    return line

write_to_csv([headers_assemble(['Date','Flight','Program','Number','Class','Fare','From','To'])]+fare_csv_list,'fare_programm_test')

print("Finished!!!!!!")
