import re
from datetime import datetime

def generuj_raport (destination):
    file = open(destination, "r")
    lines = file.readlines()
    correct_logs_p = []
    correct_logs = []
    incorrect_logs = []
    for line in lines:
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}\s\d+')
        if pattern.match(line):
            x = line.strip("\n")
            correct_logs_p.append(x)
        else:
            x = line.strip("\n")
            incorrect_logs.append(x)
    for log in correct_logs_p:
        try:
            datetime.strptime(log[:16], '%Y-%m-%d %H:%M')
            correct_logs.append(log)
        except ValueError:
            incorrect_logs.append(log)

    if len(incorrect_logs) > 0:
        list_1 = len(lines)
        list_2 = len(incorrect_logs)
        count = round((list_2/list_1)*100, 1)
    else:
        count = 100

    correct_time = []

    if len(correct_logs) > 0:
        for position in correct_logs:
            element = position.split(" ")
            time = element[0] + " " + element[1]
            correct_time.append(time)
        string_1 = correct_time[0]
        string_2 = correct_time[-1]
        datetime_object1 = datetime.strptime(string_1, '%Y-%m-%d %H:%M')
        datetime_object2 = datetime.strptime(string_2, '%Y-%m-%d %H:%M')
        delta = datetime_object2 - datetime_object1
        duration = delta.total_seconds() / 60
        ints = []
        temperature = []

        for position2 in correct_logs:
            elements = position2.split(" ")
            temperature_list = elements[2].strip("C")
            temperature.append(temperature_list)

        for element in temperature:
            ints.append(float(element))

        ints.sort()
        temp_max = max(ints)
        temp_min = min(ints)
        temp_avg = round(sum(ints) / len(ints), 1)

        splitted_logs = []
        for i in correct_logs:
            splitted = i.split(" ")
            splitted_date = splitted[0]+" "+splitted[1]
            x = datetime.strptime(splitted_date, '%Y-%m-%d %H:%M'),float(splitted[2].strip("C"))
            splitted_logs.append(x)

        sequence = []
        times = []
        y = False
        splitted_logs.sort()
        for i in splitted_logs:
            if i[1] > 100 and y == False:
                sequence.append(i)
                y = True
            elif i[1] > 100 and y == True and i[1] != splitted_logs[-1][1]:
                sequence.append(i)
            elif i[1] > 100 and y == True and i[1] == splitted_logs[-1][1]:
                sequence.append(i)
                sequence.sort()
                times.append((sequence[-1][0] - sequence[0][0]).total_seconds()/60)
                sequence.clear()
            elif i[1] < 100 and y == True:
                sequence.sort()
                times.append((sequence[-1][0] - sequence[0][0]).total_seconds()/60)
                sequence.clear()

        if len(times) > 0:
            ret_times = len(times)
        else:
            ret_times = 0

        overheat = int(times[-1])

        if overheat > 10:
            overheat_risk = True
        else:
            overheat_risk = False

    else:
        duration = 0
        temp_max = None
        temp_min = None
        temp_avg = None
        overheat = 0
        overheat_risk = False

    if round(count, 1) > 10:
        noise = True
    else:
        noise = False


    if len(times) > 0:
        ret_times = len(times)
    else:
        ret_times = 0

    overheat = int(times[-1])

    dictionary = {
            "wadliwe_logi": incorrect_logs,
            "procent_wadliwych_logow": str(count),
            "czas_trwania_raportu": int(duration),
            "temperatura": {
                "max": str(temp_max),
                "min": str(temp_min),
                "srednia": str(temp_avg)
            },
            "najdluzszy_czas_przegrzania": overheat,
            "liczba_okresow_przegrzania": int(ret_times),
            "problemy": {
                "wysoki_poziom_zaklocen_EM": noise,
                "wysokie_ryzyko_uszkodzenia_silnika_z_powodu_temperatury": overheat_risk
            }
        }



    for keys, values in dictionary.items():
        print(keys, values)




    return dictionary
generuj_raport("input.txt")