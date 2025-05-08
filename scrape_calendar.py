import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
import datetime
import pytz
import os
import re

# Create a calendar
cal = Calendar()
cal.add('prodid', '-//My Calendar Scraper//example.com//')
cal.add('version', '2.0')

# URL of the calendar page
url = "https://prestigestar.cincwebaxis.com/your-calendar-page"  # Replace with actual URL

# Send a request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all appointment divs
appointments = soup.find_all('div', class_='dxscApt')

# Process each appointment
for appointment in appointments:
    event = Event()
    
    # Extract title
    title_span = appointment.find('span', id=re.compile('.*lblTitle$'))
    if title_span:
        event.add('summary', title_span.text)
    
    # Extract start and end times
    start_time_span = appointment.find('span', id=re.compile('.*lblStartTime$'))
    end_time_span = appointment.find('span', id=re.compile('.*lblEndTime$'))
    
    if start_time_span and end_time_span:
        # You'll need to extract date from elsewhere in the page
        # For now using today's date as placeholder
        today = datetime.date.today()
        
        # Parse times (assuming format like "9:00 AM")
        start_time_str = start_time_span.text
        end_time_str = end_time_span.text
        
        # Convert to datetime objects (basic implementation)
        start_hour, start_minute = map(int, start_time_str.split(':')[0:2])
        if "PM" in start_time_str and start_hour != 12:
            start_hour += 12
        if "AM" in start_time_str and start_hour == 12:
            start_hour = 0
            
        end_hour, end_minute = map(int, end_time_str.split(':')[0:2])
        if "PM" in end_time_str and end_hour != 12:
            end_hour += 12
        if "AM" in end_time_str and end_hour == 12:
            end_hour = 0
        
        start_dt = datetime.datetime.combine(today, datetime.time(start_hour, start_minute))
        end_dt = datetime.datetime.combine(today, datetime.time(end_hour, end_minute))
        
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
    
    # Extract location if available
    title_text = title_span.text if title_span else ""
    location_match = re.search(r'\((.*?)\)', title_text)
    if location_match:
        event.add('location', location_match.group(1))
    
    # Add event to calendar
    cal.add_component(event)

# Write calendar to file
with open('my_calendar.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Calendar file created: my_calendar.ics")
