from datetime import datetime

def get_date_path():
    '''
    Function for getting the folder name for today temperature

    Parameters:
        None

    Returns:
        str: date
    '''

    today = datetime.now()
    month_day = today.strftime("%m-%d")
    date = str(today.year-2) + "-" + month_day
    return date