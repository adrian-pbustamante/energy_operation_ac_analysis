import zipfile
import pandas as pd
import os

##Define the root directory for data (adjust if necessary)
ROOT_DIR = './'
DATA_RAW_PATH = os.path.join(ROOT_DIR, 'data_raw')
DATA_OUTPUT_PATH = os.path.join(ROOT_DIR, 'data_output')

def ensure_output_directory():
    """makes sure the output directory exists"""
    if not os.path.exists(DATA_OUTPUT_PATH):
        os.makedirs(DATA_OUTPUT_PATH)
        print(f"Created directory: {DATA_OUTPUT_PATH}")

def extract_zip(zip_file, destination_path = DATA_RAW_PATH):
    """EXtracts zip file to destination_path"""
    zip_path = os.path.join(DATA_RAW_PATH, zip_file)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination_path)
        print(f'Successfully extracted {zip_file}')
    except FileNotFoundError:
        print(f"Error: Zip file not found at {zip_path}")
    except Exception as e:
        print(f"Error extracting {zip_file}: {e}")

def process_ac_data(data_path=DATA_RAW_PATH):
    """ Processes individual AC unit excel files, clean the data, adds the AC unit name,
    and combines them into Base1.xlsx"""

    print("\n------Processing  AC units data (Base 1)----")
    extract_zip('Aires Acondicionados.zip')

    AC_dataframes = {}
    for filename in os.listdir(data_path):
        if filename.startswith('AC') & filename.endswith('.xlsx'):
            file_path = os.path.join(data_path, filename)
            df = pd.read_excel(file_path)
            
            #add unit name
            df['Unidad de AC'] = filename[:-5] ##exclusdes '.xlsx' in the name

            #clean and rename columns
            df = df.loc[4:].reset_index(drop=True).rename(
                columns = {'Log Data':'Fecha', 'Unnamed: 1': 'Encendido'}
            )
            #format date
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df['Fecha'] = df['Fecha'].dt.strftime('%b %d, %Y %I:%M:%S %p')

            #add to dictionary
            AC_dataframes[filename] = df 

    #concatenate all AC data frames
    output_df = pd.DataFrame()
    #sort keys numerically 
    sorted_ac = dict(sorted(AC_dataframes.items(), key=lambda x: int(x[0][2:-5])))

    for key in sorted_ac:
        output_df = pd.concat([output_df, sorted_ac[key]], ignore_index=True, axis=0)

    #save output
    output_path = os.path.join(DATA_OUTPUT_PATH, 'Base1.xlsx')
    output_df.to_excel(output_path, index=False)
    print(f"Base1 (AC Unit status) saved to {output_path}")
    return None

def process_energy_data(data_path = DATA_RAW_PATH):
    """Process energy files, cleans the data, merges AC and General Energy, 
    and saves the result in Base2"""

    print("\n--- Processing Energy Data (Base2)----")
    extract_zip('Energia.zip')

    #read and process AC energy
    ener_ac = pd.read_excel(os.path.join(data_path, 'Energia AC.xls'))
    ener_ac = ener_ac.rename(columns={'Date & Time': 'date_time', 'AIRE ACONDICIONADO->User Win Total(kWh)': 'AC_energy(kWh)'})
    ener_ac['date_time'] = pd.to_datetime(ener_ac['date_time']).dt.strftime('%Y-%m-%d %H:%M')
    ener_ac = ener_ac.sort_values(by='date_time', ascending=False).reset_index(drop=True)

    ##read and process general energy
    ener = pd.read_excel(os.path.join(data_path, 'Energía General.xls'))
    ener = ener.rename(columns = {'Date & Time': 'date_time', 'Medición General->User Win Total(kWh)': 'general_energy(kWh)'})
    ener['date_time'] = pd.to_datetime(ener['date_time']).dt.strftime('%Y-%m-%d %H:%M')
    ener = ener.sort_values(by='date_time', ascending=False).reset_index(drop=True)

    #merge, left join in general energy since it has more observations
    output2 = ener.merge(ener_ac, on='date_time', how='left')

    #save output
    output_path = os.path.join(DATA_OUTPUT_PATH, 'Base2.xlsx')
    output2.to_excel(output_path, index=False)
    print(f"Base2 (energy merged) save to {output_path}")
    return output2

def process_temp_data(base2_df, data_path = DATA_RAW_PATH):
    """Processes ext temperature data, cleans it and merges it with Base2, creates Base3.xlsx
    and temperature.xlsx"""

    print("\n--- Processing temperature data---")
    temp_ext = pd.read_excel(os.path.join(data_path, 'Temp Ext.xlsx'))
    #rename and clean
    temp_ext = temp_ext.rename(columns = {'Log Data':'date_time', 'Unnamed: 1': 'celcius'})
    temp_ext = temp_ext[4:].reset_index(drop=True)

    #format datetime
    temp_ext['date_time'] = pd.to_datetime(temp_ext['date_time'])
    temp_ext['date_time'] = temp_ext['date_time'].dt.strftime('%Y-%m-%d %H:%M')

    #merge with base 2, user inner join only uses times that appear in both base2 and temp_ext
    output = base2_df.merge(temp_ext, on='date_time', how='inner')

    #save output
    output_path = os.path.join(DATA_OUTPUT_PATH, 'Base3.xlsx')
    output.to_excel(output_path, index=False)
    output_path = os.path.join(DATA_OUTPUT_PATH, 'temperature.xlsx')
    temp_ext.to_excel(output_path, index=False)
    print(f"Base2 and temperature saved to {output_path}")
    return None

def main_etl():
    """main function to run the etl process"""
    ensure_output_directory()
    
    process_ac_data() ##base1
    df_base2 = process_energy_data() ##base2
    process_temp_data(df_base2) #base3, temperature

    print("\n ETL process complete")

if __name__=='__main__':
    main_etl()
    






    










    
        




















            