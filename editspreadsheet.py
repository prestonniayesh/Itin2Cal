import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("sheetscreds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Itinerary Formatter").sheet1

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August": 8, "September":9, "October":10, "November":11, "December":12}

def findday(line):
    line_iter = iter(line)
    try:
        word = ""
        while True:
            char = next(line_iter)
            if char == " " or char == ",":
                if len(word) != 0 and word in days:
                    return word
                word = ""
            else:
                word += char
    except StopIteration:
        if len(word) != 0 and word in days:
            return word

def next2chars(line_iter):
    return next(line_iter) + next(line_iter)

def nextday(line_iter):
    rest = list(line_iter)
    wspacei = rest.index(" ")
    letters = rest[:wspacei]
    day = ""
    for letter in letters:
        day += letter
    return day

def finddayseries(line):
        line_iter = iter(line)
        try:
            word = ""
            while True:
                char = next(line_iter)
                if char == " " or char == ",":
                    if len(word) != 0 and word in days and next2chars(line_iter) == "- ":
                        return word + " " + nextday(line_iter)
                    word = ""
                else:
                    word += char
        except StopIteration:
            return

def date2num(date):
    wspacei = date.find(" ")
    month = date[:wspacei]
    monthnum = months[month]
    daynum = date[len(month) + 1: len(month) + 2]
    return str(monthnum) + "/" + str(daynum) + "/2020"

itinerary = open("2020 Pac-12 Championships Itinerary", "r").readlines()
for line in itinerary:
    day = findday
    if day:
        date = date2num(line[len(day) + 2:-2])
        












print("Hello world")
