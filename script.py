import os
import statistics
def build_list_google(start_time, end_time, input_file):
    f = open(input_file, 'r')

    locations = []
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            new = line.replace('"', "").split(",")
            timestamp = int(new[0])
            if (timestamp > start_time and timestamp < end_time):
                loc_time = int(new[1])
                lat = float(new[2])
                lon = float(new[3])
                prov = new[5]
                lst = [timestamp, loc_time, lat, lon, prov]
                locations.append(lst)
    f.close()
    return locations

def build_list_jedai(start_time, end_time, input_file):
    f = open(input_file, 'r')

    locations = []
    for line in f: 
        if "NetworkLocationReceiver" in line:
            new = line.replace('"', "").split()
            timestamp = int(new[0])
            if (timestamp > start_time and timestamp < end_time):
                coords = new[10].split(",")
                lat = float(coords[0])
                lon = float(coords[1])
                lst = [timestamp, lat, lon]
                locations.append(lst)
    f.close()
    return locations

def build_dict_user(input_file):
    f = open(input_file, 'r')

    locations_user = {}
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else: 
            new = line.replace('"', "").split(",")
            locations_user[new[0]]=int(new[1])
    f.close()
    return locations_user

def build_list_phone_events(start_time, end_time, input_file):
    f = open(input_file, 'r')

    events = []
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            new = line.replace('"', "").split(",")
            print(new)
            timestamp = int(new[0])
            if (timestamp > start_time and timestamp < end_time):
                events.append([timestamp, new[1]])
    return events

def jedai_stats(jedai_locs, enter_time, exit_time):
    wakes = []
    unique_locs = []
    poi_locs = []

    prev_wake = jedai_locs[0][0]
    prev_lat = jedai_locs[0][1]
    prev_lon = jedai_locs[0][2]
    for loc in jedai_locs:
        curr_wake = loc[0]
        curr_lat = loc[1]
        curr_lon = loc[2]
        diff = curr_wake - prev_wake
        if (curr_lat != prev_lat or curr_lon != prev_lon):
            unique_locs.append([curr_wake, (curr_lat, curr_lon)])
            if (curr_wake > enter_time and curr_wake < exit_time):
                poi_locs.append([curr_wake, (curr_lat, curr_lon)])
        wakes.append(diff)
        prev_wake = curr_wake
        prev_lat = curr_lat
        prev_lon = curr_lon
    
    num_wakes = len(wakes)
    average_wake = float(sum(wakes))/num_wakes
    print()
    print(statistics.median(wakes))
    print("Number of wakes of JedAI: " + str(num_wakes))
    print("Average wake time of JedAI: " + str(average_wake))
    print("Number of unique locations of JedAI: " + str(len(unique_locs)))
    print("Number of POI locations of JedAI: " + str(len(poi_locs)))
    print()
    return unique_locs

def google_stats(google_locs, enter_time, exit_time):
    wakes = {"gps": [], "network": [], "fused": []}
    unique_locs = {"gps": [], "network": [], "fused": []}
    poi_locs = {"gps": [], "network": [], "fused": []}
    prev_wake = {"gps": 0, "network": 0, "fused": 0}
    prev_lat = {"gps": 0, "network": 0, "fused": 0}
    prev_lon = {"gps": 0, "network": 0, "fused": 0}

    for loc in google_locs:
        curr_wake = loc[0]
        curr_lat = loc[2]
        curr_lon = loc[3]
        loc_type = loc[4]
        if prev_wake[loc_type] == 0:
            prev_wake[loc_type] = curr_wake
            prev_lat[loc_type] = curr_lat
            prev_lon[loc_type] = curr_lon
        diff = curr_wake - prev_wake[loc_type]
        wakes[loc_type].append(diff)
        if not (curr_lat == prev_lat[loc_type] and curr_lon == prev_lon[loc_type]):
            unique_locs[loc_type].append([curr_wake, (curr_lat, curr_lon)])
            if (curr_wake > enter_time and curr_wake < exit_time):
                poi_locs[loc_type].append([curr_wake, (curr_lat, curr_lon)]) 
        prev_wake[loc_type] = curr_wake
        prev_lat[loc_type] = curr_lat
        prev_lon[loc_type] = curr_lon
    
    print(statistics.median(wakes['gps']))
    print(statistics.median(wakes['network']))
    print(statistics.median(wakes['fused']))
    num_wakes = [len(wakes['gps']), len(wakes['network']), len(wakes['fused'])]
    average_wakes = [
        sum(wakes['gps'])/num_wakes[0], 
        sum(wakes['network'])/num_wakes[1],
        sum(wakes['fused'])/num_wakes[2],  
    ]
    num_unique_locs = [
        len(unique_locs['gps']),
        len(unique_locs['network']),
        len(unique_locs['fused'])
    ]
    num_poi_locs = [
        len(poi_locs['gps']),
        len(poi_locs['network']),
        len(poi_locs['fused'])
    ]
    
    print("Number of wakes of gps: " + str(num_wakes[0]))
    print("Average wake time of gps: " + str(average_wakes[0]))
    print("Number of unique locations of gps: " + str(num_unique_locs[0]))
    print("Number of POI locations of gps: " + str(num_poi_locs[0]))

    print()
    print("Number of wakes of network: " + str(num_wakes[1]))
    print("Average wake time of network: " + str(average_wakes[1]))
    print("Number of unique locations of network: " + str(num_unique_locs[1]))
    print("Number of POI locations of network: " + str(num_poi_locs[1]))

    print()
    print("Number of wakes of fused: " + str(num_wakes[2]))
    print("Average wake time of fused: " + str(average_wakes[2]))
    print("Number of unique locations of fused: " + str(num_unique_locs[2]))
    print("Number of POI locations of fused: " + str(num_poi_locs[2]))
    print()

    return (unique_locs)

def file_finder(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    raise ("File not found-"+substring)

def main():
    curr_dir = os.listdir()
    google_loc_filename = curr_dir[file_finder(curr_dir, 'google_locations')]
    jedai_loc_filename = curr_dir[file_finder(curr_dir, 'main-')]
    user_input_filename = curr_dir[file_finder(curr_dir, 'user_input')]
    phone_events_filename = curr_dir[file_finder(curr_dir, 'phone_events')]

    user_events = build_dict_user(user_input_filename)
    start_time = user_events['poi_collect_start'] 
    end_time = user_events['poi_collect_stop']
    enter_time = user_events['poi_collect_enter']
    exit_time = user_events['poi_collect_exit']

    jedai_locs = build_list_jedai(start_time, end_time, jedai_loc_filename)
    google_locs = build_list_google(start_time, end_time, google_loc_filename)
    phone_events = build_list_phone_events(start_time, end_time, phone_events_filename)

    unique_jedai_locs = jedai_stats(jedai_locs, enter_time, exit_time)
    unique_google_locs = google_stats(google_locs, enter_time, exit_time)

    total_unique_locs = unique_google_locs.copy()
    total_unique_locs['JedAI'] = unique_jedai_locs
    total_unique_locs['phone_event'] = phone_events

    total_by_time = []
    for source in total_unique_locs:
        for loc in total_unique_locs[source]:
            total_by_time.append(loc + [source])

    sorted_total_uniques = sorted(total_by_time)
    for entry in sorted_total_uniques:
        print(entry)

main()
