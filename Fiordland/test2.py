Emergency_Freezer = 'Back up plan in which I have to rent a truck, but a chest freezer, and move it to GNS Dunedin / ' \
                    'and move all my samples there. '

# Contingency Planning
if 'CoolTranz agrees to the frozen shipment (in general)':
    if 'CoolTranz quote is within the budget constraints of Marcus':
        if 'the pickup date is NOT flexible':
            if 'the ship shows up ON TIME on June 10':
                result = 'ideal'
            elif 'the ship DOESNT SHOW UP ON TIME on June 10':
                result1 = 'I have to cancel my flights, book accomodation, liase with CoolTranz'
                result2 = 'I have to cancel my flights, book accomodation, cancel CoolTranz, initiate plan Emergency Freezer'
                if result2:
                    downstream = 'Ill have to figure out a way to secure the freezer in case of power outages,' \
                                 ' or plan some way to move the samples up here at a later stage'

        elif 'the pickup date IS flexible':
            if 'the ship shows up ON TIME on June 10':
                result = 'ideal'
            elif 'the ship DOESNT SHOW UP ON TIME on June 10':
                result1 = 'I have to cancel my flights, book accomodation, but at least now theyll still come get it'

    elif 'CoolTranz quote is NOT within the budget constraints of Marcus (too expensive)':
        result = 'I ship my freezer from here to GNS Dunedin, store them temporarily down there.' \
                 ' Ill also have to deal with power outages'

"""
The cost of the backup plan (i.e., the cost of the ship not showing up to the dock on time is:
AT BEST == the sum of 1) renting a truck 2) buying a chest freezer 3) IT setting up a phone system to call me if the power goes out
AT WORST == the samples thaw and are lost. 
"""