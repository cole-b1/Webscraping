from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from plotly.graph_objs import Bar
from plotly import offline

best_ppg = 0
worst_ppg = 1000000
best_year_ppg = 0
worst_year_ppg = 1000000

best_pass_yards = 0
worst_pass_yards = 1000000
best_year_pass = 0
worst_year_pass = 1000000

best_conv = 0
worst_conv = 1000000
best_conv_year = 0
worst_conv_year = 1000000

best_fg = 0
worst_fg = 1000000
best_fg_year = 0
worst_fg_year = 1000000

total_attendance = 0
attendance_dict = {}
years_processed = 0
for year in range(2016, 2025):
    years_processed += 1
    url = f'https://cfbstats.com/{year}/team/51/index.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    req = Request(url, headers=headers)

    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    table1 = soup.findAll('table')[0]
    table2 = soup.findAll('table')[1]

    table_rows1 = table1.findAll('tr')
    table_rows2 = table2.findAll('tr')

    
    for row in table_rows1[1:]:
        
        category = row.findAll('td')[0].text.strip()
        stat = row.findAll('td')[1].text.strip()
        

        if category == 'Scoring:  Points/Game':
            

            if '.' in stat and stat.replace('.', '', 1).isdigit():  
                stat_value = float(stat)
                if stat_value > best_ppg:
                    best_ppg = stat_value
                    best_year_ppg = year
                if stat_value < worst_ppg:
                    worst_ppg = stat_value
                    worst_year_ppg = year

        

        if category == 'Passing:  Yards':
            
            
                stat_value = float(stat)
                if stat_value > best_pass_yards:
                    best_pass_yards = stat_value
                    best_year_pass = year
                if stat_value < worst_pass_yards:
                    worst_pass_yards= stat_value
                    worst_year_pass = year



        if category == '3rd Down Conversions: Conversion %':


            stat = stat.replace('%', '').strip()
    
            stat_value = float(stat)
            if stat_value > best_conv:
                best_conv = stat_value
                best_conv_year = year
            if stat_value < worst_conv:
                worst_conv = stat_value
                worst_conv_year = year



        if category == 'Field Goals:  Success %':


            stat = stat.replace('%', '').strip()
    
            stat_value = float(stat)
            if stat_value > best_fg:
                best_fg = stat_value
                best_fg_year = year
            if stat_value < worst_fg:
                worst_fg = stat_value
                worst_fg_year = year



#Plotly


    for row in table_rows2[1:]:
            tds = row.findAll('td')

            
            if len(tds) >= 5:
                opponent = tds[1].text.strip()
                opponent = opponent.replace('+', '').replace('@', '').strip(' 0123456789')
                
                attendance = tds[4].text.strip().replace(",", "")
                if attendance.isdigit():
                    attendance = int(attendance)
                else:
                    attendance = 0
                attendance_dict[opponent] = attendance_dict.get(opponent, 0) + attendance
                
sorted_attendance = sorted(attendance_dict.items(), key=lambda x:x[1], reverse=True)[:5]

print(f'Best PPG occurred in the year: {best_year_ppg}')
print(f'Worst PPG occurred in the year: {worst_year_ppg}')
print(f'Best Passing Yards occurred in the year: {best_year_pass}')
print(f'Worst Passing Yards occurred in the year: {worst_year_pass}')
print(f'Best 3rd Down Conversion % occurred in the year: {best_conv_year}')
print(f'Worst 3rd Down Conversion % occurred in the year: {worst_conv_year}')
print(f'Best Field Goal % in the year: {best_fg_year}')
print(f'Worst Field Goal % in the year: {worst_fg_year}')
print()
teams = [item[0] for item in sorted_attendance]
attendance_values = [item[1] for item in sorted_attendance]

for team, attendance in sorted_attendance:
    print(f"{team}: {attendance:,} attendees")
    print()

data = [{
    'type': 'bar',
    'x': teams,
    'y': attendance_values,
    'marker': {
        'color': 'green',
    },
    'width': .8,
    'opacity': 0.6,
}]

mylayout = {
    'title': 'Biggest Rivalry Based on Attendance',
    'xaxis': {'title': 'Teams'},
    'yaxis': {'title': 'Attendance'},
    'plot_bgcolor': 'gold',
    'width': 1080,
    'height': 720,
}

fig = {'data': data, 'layout': mylayout}
offline.plot(fig,filename = 'rivalry_chart.html')


