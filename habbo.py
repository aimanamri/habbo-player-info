import requests
from datetime import datetime, timezone

def read_player_data(username):
    try:
        res = requests.get('https://www.habbo.com/api/public/users?name='+str(username))
        return res.json()
    except:
        return 'Issue with accessing API'

def compute_human_last_login(last_access_time):
    """
    Convert a player's last access time into a human readable 
    format - days, hours, minutes: returns a tuple.
    """
    # Slice the date/time String into date and time components.
    # 2018-00-00T00:00:00.000+0000 -> 2018-00-00, 00:00
    date_lastAccessTime = last_access_time[:(last_access_time.find('T'))]
    time_lastAccessTime = last_access_time[(last_access_time.find('T') + 1):(last_access_time.find('.'))]
    date_time_lastAccessTime = date_lastAccessTime + ' ' + time_lastAccessTime

    # Convert the sliced strings into a datetime object in order to compute the difference in hours.
    FMT = '%Y-%m-%d %H:%M:%S'
    current_date_time_obj = datetime.strptime((datetime.now(timezone.utc).strftime(FMT)), FMT)
    date_time_obj = datetime.strptime(date_time_lastAccessTime, FMT)
    
    date_time_diff = current_date_time_obj - date_time_obj

    return f'{date_time_diff.days} day(s)', f'{(date_time_diff.seconds // 3600)} hour(s)', f'{(date_time_diff.seconds // 60 % 60)} minutes'

def get_player_attributes(username):
    player_data = read_player_data(username)

    try:
        username = player_data['name']
        motto = player_data['motto']
        is_profile_visible = player_data['profileVisible']
        
        if is_profile_visible:
            is_online = player_data['online']
            last_access_time = player_data['lastAccessTime']

            return username, f'Profile visibility : {is_profile_visible}', f'Motto : {motto}', f'Online now : {is_online}', [last_access_time], f'Last login:  {compute_human_last_login(last_access_time)}'
        else:
            return username, is_profile_visible, motto   
    except:
        return 'Error with accessing player'

    
if __name__ == '__main__':
    username = input('Enter habbo username :   ')
    print(get_player_attributes(username))
