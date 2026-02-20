"""
run_all.py

Master pipeline script that runs:
1. Data_quality_paper_1.py
2. Data_quality_Paper_2_2026_v1.py
3. Data_quality_Paper_3_2026.v1.py


"""

import Data_quality_paper_1
import Data_Quality_Paper_2_2026_v1
import Data_Quality_Paper_3_2026_v1


def main():
    print("Starting full pipeline...\n")

    print("Running script1...")
    Data_quality_paper_1.main()
    print("Finished script1.\n")

    print("Running script2...")
    Data_Quality_Paper_2_2026_v1.main()
    print("Finished script2.\n")

    print("Running script3...")
    Data_Quality_Paper_3_2026_v1.main()
    print("Finished script3.\n")

    print("Pipeline complete.")

if __name__ == "__main__":
    main()