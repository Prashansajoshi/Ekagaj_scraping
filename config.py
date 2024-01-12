from pyBSDate import convert_BS_to_AD
import re
from datetime import datetime 




# categories = [ 'local-government', 'politics', 'finance','science-technology','thought-interview','arts','sports',
#                 'abroad','health','weekend','children','society','education','personal','photo-feature','ekagaj-special']


categories = [ 'local-government']


start_date_str = '2024/01/01'
end_date_str = '2024/01/04'



nepali_months = {'वैशाख': 1,  'जेठ': 2, 'असार': 3, 'साउन': 4, 'भदौ': 5, 'असोज': 6,
                 'कात्तिक': 7, 'मंसिर': 8, 'पुस': 9, 'माघ': 10, 'फागुन': 11, 'चैत': 12}

nepali_years = {
    '२०७०': "2070", '२०७१': "2071", '२०७२': "2072",
    '२०७३': "2073", '२०७४': "2074", '२०७५': "2075",
    '२०७६': "2076", '२०७७': "2077", '२०७८': "2078",
    '२०७९': "2079", '२०८०': "2080", '२०८१': "2081",
    '२०८२': "2082",  '२०८३': "2083", '२०८४': "2084",
    '२०८५': "2085", '२०८६': "2086", '२०८७': "2087",
    '2088': "२०८८", '२०८९': "2089", '२०९०': "2090"
}

nepali_days = {
    '१': "1", '२': "2", '३': "3", '४': "4", '५': "5", '६': "6",
    '७': "7", '८': "8", '९': "9", '१०': "10", '११': "11", '१२': "12",
    '१३': "13", '१४': "14", '१५': "15", '१६': "16", '१७': "17", '१८': "18",
    '१९': "19", '२०': "20", '२१': "21", '२२': "22", '२३': "23", '२४': "24",
    '२५': "25", '२६': "26", '२७': "27", '२८': "28", '२९': "29", '३०': "30",
    '३१': "31", '३२': "32"
}


def parse_date(text):
   pattern = re.compile(r'(\S+)\s([०-९]+),\s([०-९]+)\b')
   match = re.search(pattern, text)
   if match:
        month = match.group(1)
        day = match.group(2)
        year = match.group(3)
        return match.group(0)
   else:
        return None


def convert_to_english(date):
    nepali_date = parse_date(date)
    # regex to separate day month and year
    pattern = re.compile(
        r'(\S+)\s([०-९]+),\s([०-९]+)\b')

    match = re.search(pattern, nepali_date)

    if match:
        month = match.group(1)
        day = match.group(2)
        year = match.group(3)

        # convert to english font
        eng_day = nepali_days[day]
        eng_month = nepali_months[month]
        eng_year = nepali_years[year]

        # convert BS date to AD date
        ad_date = convert_BS_to_AD(eng_year, eng_month, eng_day)
        return f"{ad_date[0]}/{ad_date[1]}/{ad_date[2]}"
    

def convert_to_nepali_date(english_date):
    # Convert English date to datetime object
  date_obj = datetime.strptime(english_date, '%Y/%m/%d').date()
    
    # Convert to Nepali date
  nepali_date = ad_to_bs(date_obj.year, date_obj.month, date_obj.day)
    
    # Format the Nepali date
  formatted_date = f'{nepali_date[1]} {nepali_date[2]}, {nepali_date[0]}'
    
  return formatted_date


def is_within_date_range(article_date, start_date_str, end_date_str):
    # Convert Nepali date to English date
    english_article_date = convert_to_english(article_date)
    
    # Convert English date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d').date()
    end_date = datetime.strptime(end_date_str, '%Y/%m/%d').date()

    # Check if the article date is within the specified range
    return start_date <= english_article_date <= end_date

