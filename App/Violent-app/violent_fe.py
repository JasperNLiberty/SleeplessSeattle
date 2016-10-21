def feature_engineer(X):

    #Get unique zone names and use them to populate new indicator variables
    zone_names = ['D2', 'R3', 'J2', 'B2', 'C1', 'N1', 'K1', 'Q3', 'M3', 'U3', 'M2',
      'N3', 'E1', 'J3', 'B3', 'D1', 'Q1', 'C2', 'F1', 'L2', 'E3', 'G3',
      'D3', 'W1', 'O2', 'Q2', 'S2', 'F2', 'K3', 'W3', 'N2', 'F3', 'U2',
      'B1', 'R1', 'J1', 'O1', 'L1', 'K2', 'M1', 'S1', 'O3', 'E2', 'S3',
      'G1', 'C3', 'W2', 'G2', 'L3', 'U1', 'R2', 'W', 'DS', '99', 'E',
      'BS', 'S', 'WP', 'US', 'MS', 'FS', 'KS', 'WS', 'OS', 'N', 'CTY',
      'KCIO07', 'SS', 'CS', 'DET', 'TRF', 'JS', 'EP', 'LS', 'H3', 'RS',
      'NP', 'INV', 'EDD', 'COMM', 'ES', 'GS', 'CCD', 'SCTR1', 'NS', 'QS']

    for zone in zone_names:
       X[zone] = 0
       X.loc[X['Zone/Beat'] == zone, zone] = 1

    #Create month dummies
    month_names = {1.0: "January", 2.0: "February", 3.0: "March", 4.0: "April", 5.0: "May", 6.0: "June", 7.0: "July", 8.0: "August", 9.0: "September", 10.0: "October", 11.0: "November", 12.0: "December"}
    months = [1.,   6.,   9.,   2.,   8.,   7.,   5.,   4.,   3.,  10.,  11., 12.]

    for month in months:
        X[month_names[month]] = 0
        X.loc[X['Scene_Month'] == month, month_names[month]] = 1

    #And for day of week
    day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    daysofweek = [ 6.,  3.,  2.,  1.,  5.,  4.,  0.]
    
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
