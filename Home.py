import streamlit.components.v1 as stc
from Dashboard import run_dashboard_app
from Prediksi_BKPN import run_predict_app
import streamlit as st


st.set_page_config(page_title="Pemodelan Prediktif untuk Penentuan Status Akhir BKPN",
                   layout="wide")

# Custom CSS
custom_css = """
<style>
    body {
        font-family: Arial, sans-serif;
    }
    .main-header {
        background-color: #131842;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .main-header h3 {
        margin: 5px;
    }
    .content-padding {
        padding: 20px;
    }
</style>
"""

# Custom HTML
html_temp = """
    <div class="main-header">
        <h3>Pemodelan Prediktif Status Akhir BKPN</h3>
        <h3>Kelompok 2</h3>
    </div>
"""

def main():
    stc.html(custom_css + html_temp)
    menu = ["Home", "Prediction", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.write('##### Deployment ini dibuat untuk kepentingan Action Learning PJJ Data Analytics Kelompok 2')
        st.write('### Problem Statement')
        st.write('Dalam pengurusan BKPN, KPKNL belum memiliki sistem yang dapat mengukur tingkat prioritas dari sebuah berkas kasus. Hal ini dapat berdampak pada tidak efisiennya pengurusan BKPN dari segi waktu dan biaya.')
        st.write('### Objectives')
        st.markdown("""
        - Project Data Analytic ini memiliki objektif untuk menentukan apakah status piutang akan berakhir sebagai lunas atau PSBDT (Piutang Sementara Belum Dapat Ditagih).  Dengan memanfaatkan data historis dari BKPN yang sudah tidak aktif di Kanwil DJKN Banten, project ini menggunakan Machine Learning dalam melakukan Predictive Modelling.
        - Tujuannya adalah untuk membantu Pemangku Kepentingan dan KPKNL dalam menetapkan prioritas penyelesaian pengurusan piutang negara.
        - Diharapkan, model ini dapat mempercepat proses penyelesaian dan dapat meningkatkan efektivitas pengurusan dengan memastikan bahwa BKPN yang memiliki kemungkinan tinggi untuk diselesaikan mendapatkan prioritas utama.
        """)
    elif choice == "Prediction":
        run_predict_app()
    elif choice == "Dashboard":
        run_dashboard_app()

if __name__ == '__main__':
    main()