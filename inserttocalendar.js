function itinerary() {

  var spreadsheet = SpreadsheetApp.getActiveSheet();
  var calendarId = spreadsheet.getRange("A2").getValue();
  var eventCal = CalendarApp.getCalendarById(calendarId);

  var events = spreadsheet.getRange("A5:C64").getValues();

  for (x = 0; x < events.length; x ++) {

    var shift = events[x];

    var startTime = shift[0];
    var endTime = shift[1];
    var title = shift[2];

    eventCal.createEvent(title, startTime, endTime);
  }
}
