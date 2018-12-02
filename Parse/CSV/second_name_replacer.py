import pandas as pd

df = pd.read_csv('Done/BoardingData.csv', sep = ';', header = 0)
df = df.loc[1:,] #убираем пустую строку
df.index = df.index - 1 # меняем на нумерацию от нуля

def replace_sname(df):
    count_suc = 0
    count_bad = 0
    iter = 1
    for i in range(df.shape[0]):
        print('{} from {}'.format(iter, df.shape[0]))
        sname = df.loc[i,:].SecondName
        print(sname)
        buf = ''
        if(len(sname) <= 3):
            buf = df.loc[i,:].TravelDocument
            if(df[(df.TravelDocument == df[df.index == i].TravelDocument[i]) & (df.SecondName.str.len() > 3)].TravelDocument.count() > 0):
                df.loc[i ,'SecondName'] = df[(df.TravelDocument == df[df.index == i].TravelDocument[i]) & (df.SecondName.str.len() > 3 )].SecondName.iloc[0]
                print(df.loc[i ,'SecondName'])
                count_suc +=1 
            else:
                print("Такой только один")
                count_bad +=1
        iter += 1
    print(count_suc)
    print(count_bad)
replace_sname(df)

df.to_csv('sname_replaced.csv', sep = ';', header = True, index = None)

