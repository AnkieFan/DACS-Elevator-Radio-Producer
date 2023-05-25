import billboard

def get_top_songs(year = None):    
    try:
        year = int(year)
    except:
        print("Illegal input year. Setting year to be the current.")
        year = None
    
    if(year != None and (year >= 2023 or year <2006)):
        print("The min and max supported years for the 'hot-100-songs' chart are 2006 and 2022, respectively.")
        year = None
    
    chart = billboard.ChartData('hot-100-songs', year = year)
    return chart