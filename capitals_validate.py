ALLOWED_REGIONS = [
    "africa",
    "americas",
    "asia",
    "caribbean",
    "central_america",
    "europe",
    "middle_east",
    "north_america",
    "oceania",
    "south_america",
    "southeast_asia"
]

def validate(data):
    success = True
    sorted_keys = sorted(data.keys())
    for k in sorted_keys:
        info = data[k]
        for region in info['regions']:
            if region not in ALLOWED_REGIONS:
                success = False
                print(f"Country: {k:30s} -  Region: {region} | Not in valid regions list")
    
    return success
