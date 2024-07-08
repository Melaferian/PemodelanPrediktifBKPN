import streamlit as st
import streamlit.components.v1 as components

def run_dashboard_app():
    def dashboard_page():
        # Set the custom title of the app using HTML and CSS
        st.markdown("""
            <h1 style='text-align: center; font-size: 36px;'>
                Dashboard Profil Piutang Negara Kanwil DJKN Banten
            </h1>
        """, unsafe_allow_html=True)

        # URL of the dashboard to be embedded
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNjhiNDIzNDctYjEyOS00YzEyLWI4YTAtNWYxYTAzMzJkODU1IiwidCI6ImVkNmZiMzY2LTgzMjItNDZmMy05MTVlLWM0ZDAzN2E0NTRhOSIsImMiOjEwfQ%3D%3D"

        # Embed the dashboard using an iframe and center it
        st.markdown(f"""
            <div style='display: flex; justify-content: center;'>
                <iframe src="{dashboard_url}" width="800" height="400" frameborder="0" allowFullScreen="true"></iframe>
            </div>
        """, unsafe_allow_html=True)

    # Call the function to render the dashboard page
    dashboard_page()

if __name__ == "__main__":
    run_dashboard_app()