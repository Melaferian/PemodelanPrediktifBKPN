import streamlit as st
import joblib
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import date
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def run_predict_app():        
    # Load the trained model
    model = joblib.load('rf_best.joblib')

    # Define hypothetical mean and std deviation for normalization
    mean_sp3n = 10409080 
    std_sp3n = 9752034  
    mean_usia_bkpn = 4.860586  
    std_usia_bkpn = 3.764948  
    mean_jarak_ke_kpknl = 25.078078  
    std_jarak_ke_kpknl = 73.061708  

    # KPKNL coordinates
    kpknl_coordinates = {
        "KPKNL Serang": (-6.1059278, 106.1357383),
        "KPKNL Tangerang I": (-6.177292, 106.6366305),
        "KPKNL Tangerang II": (-6.177292, 106.6366305)
    }

    # Function to get coordinates from an address
    def get_coordinates(address):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            else:
                return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Error: Geocoding service error - {e}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error occurred - {e}")
            return None
    # Function to calculate distance to KPKNL
    def calculate_distance_to_kpknl(user_coords, kpknl_choice):
        kpknl_coords = kpknl_coordinates[kpknl_choice]
        return geodesic(user_coords, kpknl_coords).kilometers

    def get_quarter(sp3n_date):
        month = sp3n_date.month
        if 1 <= month <= 3:
            return 1
        elif 4 <= month <= 6:
            return 2
        elif 7 <= month <= 9:
            return 3
        elif 10 <= month <= 12:
            return 4
        else:
            return 0  # Default case, although should not occur with valid input
    # Define a function to normalize user input
    def normalize_input(sp3n, usia_bkpn, jarak_ke_kpknl):
        norm_sp3n = (sp3n - mean_sp3n) / std_sp3n
        norm_usia_bkpn = (usia_bkpn - mean_usia_bkpn) / std_usia_bkpn
        norm_jarak_ke_kpknl = (jarak_ke_kpknl - mean_jarak_ke_kpknl) / std_jarak_ke_kpknl
        return norm_sp3n, norm_usia_bkpn, norm_jarak_ke_kpknl
    # Define a function to get user input   
    def get_user_input():
        st.sidebar.markdown("## Lengkapi Data di bawah ini.")
        # Dropdown for KPKNL choice
        kpknl_choice = st.sidebar.selectbox('Pilih KPKNL', list(kpknl_coordinates.keys()))

        sp3n = st.sidebar.number_input('Nilai Piutang', value=0, step=1)
    #
        today = date.today()
        min_date = today.replace(year=1990, month=1, day=1)  # Adjust min_date as needed
        max_date = today  # Allow current date as max date
        tanggal_sp3n = st.sidebar.date_input('Tanggal SP3N', min_value=min_date, max_value=max_date, value=min_date)
        usia_bkpn = (today - tanggal_sp3n).days / 365.25    
        # Determine the quarter based on SP3N date
        if tanggal_sp3n:
            quarter = get_quarter(tanggal_sp3n)
        else:
            quarter = 0

        st.sidebar.markdown("### Informasi alamat debitur :")
        # User inputs for location
        kelurahan = st.sidebar.text_input('Kelurahan')
        kecamatan = st.sidebar.text_input('Kecamatan')
        kabupaten_kota = st.sidebar.text_input('Kabupaten/Kota')
    
        address_found = True
        if kelurahan and kecamatan and kabupaten_kota:
            address = f"{kelurahan}, {kecamatan}, {kabupaten_kota}"
            coordinates = get_coordinates(address)
            if coordinates:
                jarak_ke_kpknl = calculate_distance_to_kpknl(coordinates, kpknl_choice)
            else:
                jarak_ke_kpknl = 0.0
                st.sidebar.error('Address not found, please check the input.')
                address_found = False
        else:
            jarak_ke_kpknl = 0.0
            address_found = False
        norm_sp3n, norm_usia_bkpn, norm_jarak_ke_kpknl = normalize_input(sp3n, usia_bkpn, jarak_ke_kpknl)

        # Assign 1 to the chosen KPKNL variable, and 0 to the others
        kpknl_serang = 1 if kpknl_choice == 'KPKNL Serang' else 0
        kpknl_tangerang_i = 1 if kpknl_choice == 'KPKNL Tangerang I' else 0
        kpknl_tangerang_ii = 1 if kpknl_choice == 'KPKNL Tangerang II' else 0
        
        # Dropdown for selecting creditor type
        kreditur = st.sidebar.selectbox('Pilih Kreditur', [
            'Badan/Lembaga Non Kemenkeu',
            'BUMN Non Perbankan',
            'DJBC',
            'Eks. BLBI',
            'Pemda',
            'Pemerintah Pusat Non Kemenkeu',
            'Perbankan',
            'Rumah Sakit',
            'STAN',
            'Sekjen Kemenkeu'
        ])
        
        # Initialize all kreditur-related variables to 0
        kred_bl_non_kemenkeu = 0
        kred_bumn_non_perbankan = 0
        kred_djbc = 0
        kred_eks_blbi = 0
        kred_pemda = 0
        kred_pp_non_kemenkeu = 0
        kred_perbankan = 0
        kred_rumah_sakit = 0
        kred_stan = 0
        kred_sekjen_kemenkeu = 0
    
        # Set the selected kreditur-related variable to 1
        if kreditur == 'Badan/Lembaga Non Kemenkeu':
            kred_bl_non_kemenkeu = 1
        elif kreditur == 'BUMN Non Perbankan':
            kred_bumn_non_perbankan = 1
        elif kreditur == 'DJBC':
            kred_djbc = 1
        elif kreditur == 'Eks. BLBI':
            kred_eks_blbi = 1
        elif kreditur == 'Pemda':
            kred_pemda = 1
        elif kreditur == 'Pemerintah Pusat Non Kemenkeu':
            kred_pp_non_kemenkeu = 1
        elif kreditur == 'Perbankan':
            kred_perbankan = 1
        elif kreditur == 'Rumah Sakit':
            kred_rumah_sakit = 1
        elif kreditur == 'STAN':
            kred_stan = 1
        elif kreditur == 'Sekjen Kemenkeu':
            kred_sekjen_kemenkeu = 1

        # Initialize terima_tw variables based on quarter
        terima_tw_i = 1 if quarter == 1 else 0
        terima_tw_ii = 1 if quarter == 2 else 0
        terima_tw_iii = 1 if quarter == 3 else 0
        terima_tw_iv = 1 if quarter == 4 else 0
        
        # Convert the user input into a format suitable for the model
        user_input = np.array([[
            sp3n, usia_bkpn, jarak_ke_kpknl,
            kpknl_serang, kpknl_tangerang_i, kpknl_tangerang_ii,
            kred_bl_non_kemenkeu, kred_bumn_non_perbankan, kred_djbc, kred_eks_blbi,
            kred_pemda, kred_pp_non_kemenkeu, kred_perbankan, kred_rumah_sakit, terima_tw_i, terima_tw_ii,
            terima_tw_iii, terima_tw_iv
        ]])
        return user_input, address_found

    # Get user input
    user_input,address_found = get_user_input()

    # Add a button to make the prediction
    if st.sidebar.button('Predict', disabled=not address_found):
        if address_found:
            # Predict using the model
            prediction = model.predict(user_input)

            # Map prediction to descriptive result
            if prediction[0] == 1:
                prediction_text = "BKPN ini diprediksikan akan **LUNAS**"
            else:
                prediction_text = "BKPN ini diprediksikan akan **PSBDT**"

            # Display the result
            st.subheader('Prediction')
            st.markdown(f'### Hasil Prediksi: {prediction_text}')
        else:
            st.markdown('### Tidak bisa membuat prediksi karena alamat tidak ditemukan.')