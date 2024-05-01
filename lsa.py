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
                leaid = row["LEAID"]
                key = (leaid, schid)
                enrollment[key] = {
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

                if leaid not in district_totals:
                    district_totals[leaid] = {race: 0 for race in ["hispanic", "native", "asian", "hp", "black", "white", "multiracial"]}

                for race in ["hispanic", "native", "asian", "hp", "black", "white", "multiracial"]:
                    district_totals[leaid][race] += enrollment[key][f"{race}_female"] + enrollment[key][f"{race}_male"]

                total_students = sum(district_totals[leaid].values())
                district_percentages[leaid] = {race: (value / total_students) * 100 for race, value in district_totals[leaid].items()}

    return enrollment, district_totals, district_percentages

def main():
    LEAID = input("Enter the LEAID number: ")
    enrollment_data, district_totals_data, district_percentages_data = load_data(LEAID)
    print("\nDistrict Totals Data:")
    for leaid, data in district_totals_data.items():
        print(f"District LEAID: {leaid}")
        for race, total in data.items():
            print(f" {race.capitalize()}: {total}")

if __name__ == "__main__":
    main()