class ExamException(Exception):
    pass



class CSVTimeSeriesFile():

    def __init__(self, name):
        self.name = name


    def get_data(self):
        
        
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            print('Errore in apertura del file: "{}"'.format(e))
            return None


        list = []

        my_file = open(self.name, 'r')
        
        for line in my_file:

            try:
                elem = line.strip().split(',')
                elem[0] = int(elem[0])
                elem[1] = float(elem[1])
            
                list.append(elem)

            except Exception:
                continue
                
        

        try:

            timestamp = 0

            for i in range(len(list)-1):
                
                if list[i][timestamp] > list[i+1][timestamp]:
                    raise ExamException("Timestamp non in ordine cronologico.")

                if list[i][timestamp] == list[i+1][timestamp]:
                    raise ExamException("Timestamp duplicato.")
                
        
        except Exception as e:
            print("ERRORE: {}".format(e))
                

        return list


def compute_daily_max_difference(time_series):
    
    temp = 1                # costanti per rendere leggibili 
    timestamp = 0           # gli indici nelle liste
    day_epoch = 86400       #   

    data = []               #conterrà i valori delle differenze di temperature
    
    diff_max = []           #conterrà i valori delle differenze di 
                            #temperature di ogni singolo giorno


    original_timestamp = time_series[0][timestamp] - (time_series[0][timestamp] % day_epoch)
    
    for item in time_series:
        
        day_start_epoch = item[timestamp] - (item[timestamp] % day_epoch)

        if original_timestamp != day_start_epoch:

            if len(diff_max) > 1: #i dati con un solo valore di temperatura non vengono salvati

                diff_max_value = max(diff_max) - min(diff_max)

                data.append(diff_max_value)
            
            elif len(diff_max) == 1:
                
                data.append(None)
            
            
            original_timestamp = day_start_epoch
            
            diff_max.clear()
        

        diff_max.append(item[temp])

    
    if len(diff_max) > 1: #perchè i dati delle ultime righe non vengono salvate nella lista

        diff_max_value = max(diff_max) - min(diff_max)

        data.append(diff_max_value)

        diff_max.clear()
    
    elif len(diff_max) == 1:
        
        data.append(None)

        diff_max.clear()


    return data

        