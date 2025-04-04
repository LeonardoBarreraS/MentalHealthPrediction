import streamlit as st
import requests

#Defining the URL of the API

url="https://mentalhealth.redriver-586a2ddd.centralus.azurecontainerapps.io/predict" #URL Azure
#url="http://127.0.0.1:8000/predict"
#url="http://localhost:8000/predict" #URL Local
#url="https://employee-turnover-a5b7b3674e44.herokuapp.com/predict" #URL Heroku



#Defining the headers

headers={"Content-Type":"application/json"}



header_html = """
    <style>
        .header-container {
            background: linear-gradient(to right, #4b6cb7, #182848);  /* Gradiente azul oscuro */
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-family: 'Arial', sans-serif;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        .header-title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
            animation: fadeIn 1.5s ease-in-out;
        }
        .header-subtitle {
            font-size: 18px;
            opacity: 0.9;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    
    <div class="header-container">
        <h1 class="header-title">🌿 Emotional Well-being Detector</h1>
        <p class="header-subtitle">Find out if you might be experiencing symptoms of depression.</p>
    </div>
"""


#Creating the main function
def main():

    #Render the HTML
    #stc.html(html_temp)
    st.markdown(header_html, unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)



    ############################################FORM CREATION###########################################################

    #Creating the columns

    col1, col_line, col2= st.columns([1,0.2,1])

    with col1:
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Gender</p>', unsafe_allow_html=True)
        Gender=st.radio("", options=["Male", "Female"])

        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Age</p>', unsafe_allow_html=True)
        Age=st.slider("",15,100,35)

        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Select your main activity</p>', unsafe_allow_html=True)
        worker_student=st.radio("", options=["Working Professional", "Student"])
        
        if worker_student=="Working Professional":
            Work_Pressure=st.slider("Work Pressure:", 1.0,5.0,2.5, format="%.1f", step=0.1)
            Job_Satisfaction=st.slider("Job Satisfaction:", 1.0,5.0,2.5, format="%.1f", step=0.1)
            Age_WorkPressure=Age*Work_Pressure
            Age_AcademicPressure=None
            Academic_Pressure=None
            Study_Satisfaction=None
        else:
            Academic_Pressure=st.slider("Academic Pressure:", 1.0,5.0,2.5, format="%.1f", step=0.1)
            Study_Satisfaction=st.slider("Study Statisfaction:", 1.0,5.0,2.5, format="%.1f", step=0.1)
            Age_AcademicPressure=Age*Academic_Pressure
            Age_WorkPressure=None
            Work_Pressure=None
            Job_Satisfaction=None
        
        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Sleep Duration</p>', unsafe_allow_html=True)
        Sleep_Duration=st.selectbox("", options=["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"])
        
        
        
    
    with col_line:
        st.markdown(
            """
            <style>
            .vertical-line {
                    border-left: 0.5px solid rgba(128, 128, 128, 0.5);  /* Línea más gruesa y negra */
                    height: 850px;  /* Altura fija para que sea visible */
                    margin-left: 25px;
                }
             </style>
            <div class="vertical-line"></div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Dietary Habits</p>', unsafe_allow_html=True)
        Dietary_Options=["Moderate", "Healthy", "Unhealthy"]
        Dietary_Habits=st.pills("", Dietary_Options, default="Moderate")

        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Academic Studies</p>', unsafe_allow_html=True)
        Academic_Studies=["High School", "Bachelor", "Master"]
        Academic_Studies=st.pills("", Academic_Studies, default="High School")
    
        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Suicidal Thoughts</p>', unsafe_allow_html=True)
        Suicidal_Thoughts=st.radio("", options=["Yes", "No"], key="Suicidal_Thoughts")

        
        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Daily Work/Study hours</p>', unsafe_allow_html=True)
        Daily_Work_Study_Hours=st.slider("", 1,15,6, step=1)

        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Financial Stress</p>', unsafe_allow_html=True)
        Financial_Stress=st.slider("",1.0,5.0,2.5, format="%.1f", step=0.1)

        st.write("")
        st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">Family History of Mental Illness</p>', unsafe_allow_html=True)
        Family_Mental_Illnes=st.radio("", options=["Yes", "No"], key="Family_Mental_Illness")

    
    ######################################################################################################################


    features={
        "Gender":Gender, 
        "Age":Age, 
        "Working_Professional_or_Student":worker_student,
        "Academic_Pressure":Academic_Pressure,
        "Work_Pressure":Work_Pressure, 
        "Study_Satisfaction":Study_Satisfaction, 
        "Job_Satisfaction":Job_Satisfaction, 
        "Sleep_Duration":Sleep_Duration, 
        "Dietary_Habits":Dietary_Habits, 
        "Degree":Academic_Studies, 
        "Suicidal_Thoughts":Suicidal_Thoughts, 
        "Work_Study_Hours":Daily_Work_Study_Hours, 
        "Financial_Stress":Financial_Stress, 
        "Family_History_of_Mental_Illness":Family_Mental_Illnes, 
        "Age_WorkPressure":Age_WorkPressure,
        "Age_AcademicPressure":Age_AcademicPressure
        }
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:20px; font-weight:bold; margin-bottom: 0.5px;">This is your selection:</p>', unsafe_allow_html=True)
    st.write(features)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Predict"):
        try:
            print("Enviando solicitud a la API...")
            response=requests.post(url, json=features, headers=headers)
                    # Verificar si la solicitud fue exitosa
            print("Código de estado de la solicitud:", response.status_code)
            if response.status_code == 200:
                depression_probability= response.json()
                st.markdown(
                    f"""
                    <div style="background-color:#d4edda; padding:10px; border-radius:5px">
                    <p style="font-size:20px; color:green; font-weight:bold">
                    ✅ Probability of Depression: {depression_probability}%
                    </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.error("Error en la solicitud. Intente de nuevo.")
                st.write("Mensaje de error:", response.text)
                st.write("Código de estado:", response.status_code)
        except requests.exceptions.RequestException as e:
            st.error("Error en la solicitudes. Intente de nuevo.")
            st.write("Mensaje de error:", e)


if __name__=="__main__":
    main()