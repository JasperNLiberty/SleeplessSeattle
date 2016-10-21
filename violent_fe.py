def feature_engineer(X):

    #Get unique zone names and use them to populate new indicator variables
    zone_names = X['Zone/Beat'].unique()

    for zone in zone_names:
       X[zone] = 0
       X.loc[X['Zone/Beat'] == zone, zone] = 1

    #Create month dummies
    month_names = {1.0: "January", 2.0: "February", 3.0: "March", 4.0: "April", 5.0: "May", 6.0: "June", 7.0: "July", 8.0: "August", 9.0: "September", 10.0: "October", 11.0: "November", 12.0: "December"}
    months = X['Scene_Month'].unique()

    for month in months:
        X[month_names[month]] = 0
        X.loc[X['Scene_Month'] == month, month_names[month]] = 1

    #And for day of week
    day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    daysofweek = X['Scene_DayofWeek'].unique()

    for day in daysofweek:
        X[day_names[day]] = 0
        X.loc[X['Scene_DayofWeek'] == day, day_names[day]] = 1

    #Create distinct variables for 3 timeslots: midnight to 5 am, 5 am to 5 pm, 5 pm to midnight
    X['Day'] = 0
    X['Evening'] = 0
    X['LateNight'] = 0

    X.loc[(X['Hour'] >=0) & (X['Hour'] <=4), 'LateNight'] = 1

    X.loc[(X['Hour'] >=5) & (X['Hour'] <= 16), 'Day'] = 1

    X.loc[X['Hour'] >= 16, 'Evening'] = 1

    X = X.drop(['Zone/Beat', 'Scene_DayofWeek', 'Scene_Month', 'Hour'], axis = 1).reset_index().copy()
    X = X.drop('index', axis = 1).copy()
    return X
