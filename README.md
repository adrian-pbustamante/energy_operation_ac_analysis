# energy_operation_ac_analysis


## Project Objective

The primary goals were:
1.  **ETL & Automation:** Build a repeatable Python pipeline to consolidate and clean operational and energy data.
2.  **Analysis:** Develop analyses to monitore operations and pinpoint posible anomalies.
3.  **Visualization & Communication:** Present key findings via a dedicated dashboard and presentation summarizing operational efficiencies.

---

### Interactive Dashboard
The dashboard allows for dynamic filtering and exploration of the data, validating historical patterns and investigating specific periods of interest.

* **View Dashboard:** [https://public.tableau.com/views/energy_temperature_dashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link]

## Repository Structure

<pre>
/main_repo_folder
├── data_raw/            # Contains original zipped files (Input)
├── data_output/         # Contains final clean Excel files (Base1.xlsx, Base2.xlsx, Base3.xlsx)
├── notebooks/           # Jupyter notebooks for initial ETL exploration and static analysis plots
├── figures/             # Static figures produced for analysis
├── report/              # Contains slides with a report of analysis
├── etl_pipeline.py      # Python script for the entire ETL process
├── README.md            # This file
└── requirements.txt     # List of required Python packages
</pre>

### How to run ETL pipeline

Clone repository to local machine
Ensure the raw data ZIP files (Aires Acondicionados.zip, Energia.zip, etc.) are placed inside the ./data_raw/ directory.
Execute the main ETL script from the root directory:

<pre>
python etl.py
</pre>

The script will automatically clean, merge, and output the final analytical files (Base1.xlsx, Base2.xlsx, Base3.xlsx) into the ./data_output/ folder.

### Summary of Core Analysis

| Finding | Metric Used | Business Implication |
| :--- | :--- | :--- |
| **Peak Demand** | Hourly Activity vs. Avg. Energy | Identified a consistent **peak energy demand hour at 19:00 hrs**. |
| **Operational Anomalies** | **Daily On_Rate ($\mu \pm 2\sigma$)** | Flagged specific days as statistically significant **outliers** (high or low usage). |
| **System Validation** | **On Rate vs. Temperature Correlation ($r=0.47$)** | Confirmed a **moderate positive correlation** between AC use and outside temperature. This validates the system's intended logic. |

---


