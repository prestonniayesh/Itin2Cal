import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("sheetscreds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Itinerary Formatter").sheet1

months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August": 8, "September":9, "October":10, "November":11, "December":12}

def date_to_num(date):
    month = date[:date.find(" ")]
    try:
        month_num = months[month]
        day_num = date[len(month) + 1: len(month) + 2]
        return str(month_num) + "/" + str(day_num) + "/2020"
    except KeyError:
        return

def convert_time(time):
    hour = int(time[:time.find(":")])
    if time.find("PM") != -1 and hour != 12 or time.find("AM") != -1 and hour == 12:
        hour += 12
    minute_str = time[time.find(":") + 1: time.find(" ")]
    if minute_str == "00":
        minute = "00"
    elif minute_str[0] == "0":
        minute = "0" + str(minute_str[1])
    else:
        minute = int(time[time.find(":") + 1: time.find(" ")])
        if minute // 10 == 0:
            minute = "0" + str(minute)
        else:
            minute = str(minute)
    return str(hour) + ":" + minute + ":00"

itinerary = open("2020 Pac-12 Championships Itinerary", "r").readlines()
starts = []
ends = []
names = []
currDate = None
count = 0
for line in itinerary:
    new_date = False
    for month in months:
        if line.find(month) != -1:
            curr_date = dateToNum(line[line.find(month):])
            new_date = True
    if new_date:
        continue
    if count > 1:
        ends.append(starts[-1])
    if line == "\n":
        ends.append(starts[-1])
        count = 0
        continue
    starts.append(curr_date + " " + convert_time(line[:8]))
    count += 1
    names.append(line[15:-1])

def update_sheet(col_num, col_name, col_list):
    sheet.update_cell(4, col_num, col_name)
    for i in range(len(col_list)):
        sheet.update_cell(i + 5, col_num, col_list[i])

update_sheet(1, "Start Time", starts)
update_sheet(2, "End Time", ends)
update_sheet(3, "Event Title", names)
