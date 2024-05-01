import csv

def load_data(LEAID):
    enrollment = {}
    district_totals = {}
    district_percentages = {}
    with open("Enrollment.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["LEAID"].lstrip("0") == LEAID:
                schid = int(row["SCHID"])
                enrollment[schid] = {
                "hispanic_female": max(0, int(row["SCH_ENR_HI_F"])),
                    "native_female": max(0, int(row["SCH_ENR_AM_F"])),
                    "asian_female": max(0, int(row["SCH_ENR_AS_F"])),
                    "hp_female": max(0, int(row["SCH_ENR_HP_F"])),
                    "black_female": max(0, int(row["SCH_ENR_BL_F"])),
                    "white_female": max(0, int(row["SCH_ENR_WH_F"])),
                    "multiracial_female": max(0, int(row["SCH_ENR_TR_F"])),
                    "hispanic_male": max(0, int(row["SCH_ENR_HI_M"])),
                    "native_male": max(0, int(row["SCH_ENR_AM_M"])),
                    "asian_male": max(0, int(row["SCH_ENR_AS_M"])),
                    "hp_male": max(0, int(row["SCH_ENR_HP_M"])),
                    "black_male": max(0, int(row["SCH_ENR_BL_M"])),
                    "white_male": max(0, int(row["SCH_ENR_WH_M"])),
                    "multiracial_male": max(0, int(row["SCH_ENR_TR_M"])),
                }
                if schid not in district_totals:
                    district_totals[schid] = {race: 0 for race in enrollment[schid].keys()}

                for demographic, count in enrollment[schid].items():
                    district_totals[schid][demographic] += count

    # Calculate percentages
    for leaid, totals in district_totals.items():
        total_students = sum(totals.values())
        district_percentages[leaid] = {demographic: (count / total_students) * 100 for demographic, count in totals.items()}

    return enrollment, district_totals, district_percentages

def load_ap_data(LEAID, district_totals):
    ap_enrollment = {}
    district_ap_totals = {}
    disparities = {}
    
    with open("Advanced Placement.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["LEAID"].lstrip("0") == LEAID:
                schid = int(row["SCHID"])
                ap_enrollment[schid] = {
                     "hispanic_female": max(0, int(row["SCH_ENR_HI_F"])),
                    "native_female": max(0, int(row["SCH_ENR_AM_F"])),
                    "asian_female": max(0, int(row["SCH_ENR_AS_F"])),
                    "hp_female": max(0, int(row["SCH_ENR_HP_F"])),
                    "black_female": max(0, int(row["SCH_ENR_BL_F"])),
                    "white_female": max(0, int(row["SCH_ENR_WH_F"])),
                    "multiracial_female": max(0, int(row["SCH_ENR_TR_F"])),
                    "hispanic_male": max(0, int(row["SCH_ENR_HI_M"])),
                    "native_male": max(0, int(row["SCH_ENR_AM_M"])),
                    "asian_male": max(0, int(row["SCH_ENR_AS_M"])),
                    "hp_male": max(0, int(row["SCH_ENR_HP_M"])),
                    "black_male": max(0, int(row["SCH_ENR_BL_M"])),
                    "white_male": max(0, int(row["SCH_ENR_WH_M"])),
                    "multiracial_male": max(0, int(row["SCH_ENR_TR_M"])),
                }
                if schid not in district_ap_totals:
                    district_ap_totals[schid] = {race: 0 for race in ap_enrollment[schid].keys()}

                for demographic, count in ap_enrollment[schid].items():
                    district_ap_totals[schid][demographic] += count

    # Calculate disparities
    for leaid, totals in district_ap_totals.items():
        for demographic, count in totals.items():
            base_count = district_totals[leaid][demographic]
            disparities[leaid][demographic] = count / base_count if base_count != 0 else 0

    return ap_enrollment, district_ap_totals, disparities

def load_suspension_data(LEAID, district_totals):
    suspension_data = {}
    district_suspension_totals = {}
    disparities = {}
    with open("Suspensions.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["LEAID"].lstrip("0") == LEAID:
                schid = int(row["SCHID"])
                suspension_data[schid] = {
                     "hispanic_female": max(0, int(row["SCH_ENR_HI_F"])),
                    "native_female": max(0, int(row["SCH_ENR_AM_F"])),
                    "asian_female": max(0, int(row["SCH_ENR_AS_F"])),
                    "hp_female": max(0, int(row["SCH_ENR_HP_F"])),
                    "black_female": max(0, int(row["SCH_ENR_BL_F"])),
                    "white_female": max(0, int(row["SCH_ENR_WH_F"])),
                    "multiracial_female": max(0, int(row["SCH_ENR_TR_F"])),
                    "hispanic_male": max(0, int(row["SCH_ENR_HI_M"])),
                    "native_male": max(0, int(row["SCH_ENR_AM_M"])),
                    "asian_male": max(0, int(row["SCH_ENR_AS_M"])),
                    "hp_male": max(0, int(row["SCH_ENR_HP_M"])),
                    "black_male": max(0, int(row["SCH_ENR_BL_M"])),
                    "white_male": max(0, int(row["SCH_ENR_WH_M"])),
                    "multiracial_male": max(0, int(row["SCH_ENR_TR_M"])),
                }
                if schid not in district_suspension_totals:
                    district_suspension_totals[schid] = {race: 0 for race in suspension_data[schid].keys()}

                for demographic, count in suspension_data[schid].items():
                    district_suspension_totals[schid][demographic] += count

    # Calculate disparities
    for leaid, totals in district_suspension_totals.items():
        for demographic, count in totals.items():
            base_count = district_totals[leaid][demographic]
            disparities[leaid][demographic] = count / base_count if base_count != 0 else 0

    return suspension_data, district_suspension_totals, disparities

