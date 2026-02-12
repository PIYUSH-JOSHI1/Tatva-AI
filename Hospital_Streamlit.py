import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import pickle
import os
from io import BytesIO
import pydicom
import cv2
import random
from ultralytics import YOLO
from plotly.subplots import make_subplots

# ============================================
# CUSTOM CSS LOADER
# ============================================
def load_custom_css():
    """Load custom CSS for improved UI"""
    css_file = "custom_styles.css"
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline CSS if file not found
        st.markdown("""
        <style>
        /* Fallback minimal styling */
        .stButton > button {
            background: linear-gradient(135deg, #2E86DE 0%, #1B4F72 100%);
            color: white;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(46, 134, 222, 0.4);
        }
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #262B3D 0%, #1A1D29 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #3E4555;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        h1 {
            background: linear-gradient(135deg, #5DADE2 0%, #2E86DE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
        """, unsafe_allow_html=True)

# ============================================
# UTILITY FUNCTIONS
# ============================================
def show_page_header(title, subtitle="", icon="🏥"):
    """Display a professional page header"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon} {title}</h1>
        <p style="color: #B8BCC8; font-size: 1.1rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_info_card(title, content, color="#2E86DE"):
    """Create a styled information card"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(46, 134, 222, 0.1) 0%, rgba(46, 134, 222, 0.05) 100%);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h3 style="margin-top: 0; color: {color};">{title}</h3>
        <p style="margin-bottom: 0; color: #FAFAFA;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

# Load languages
def load_languages():
    return {
        'English': {
            'welcome': 'Welcome',
            'dashboard': 'Dashboard',
            'profile': 'Profile',
            'settings': 'Settings',
            'emergency': 'Emergency Contact',
            'about': 'About Us',
            'prediction': 'Patient Prediction',
            'analytics': 'Analytics'
        },
        'Spanish': {
            'welcome': 'Bienvenido',
            'dashboard': 'Tablero',
            'profile': 'Perfil',
            'settings': 'Ajustes',
            'emergency': 'Contacto de Emergencia',
            'about': 'Sobre Nosotros',
            'prediction': 'Predicción de Pacientes',
            'analytics': 'Análisis'
        },
        'French': {
            'welcome': 'Bienvenue',
            'dashboard': 'Tableau de Bord',
            'profile': 'Profil',
            'settings': 'Paramètres',
            'emergency': 'Contact d\'urgence',
            'about': 'À Propos',
            'prediction': 'Prédiction de Patients',
            'analytics': 'Analytique'
        }
    }

# Theme configurations
dark_theme = {
    'primary_color': '#4da6ff',
    'background_color': '#0e1117',
    'secondary_bg': '#262730',
    'text_color': '#fafafa',
    'font': 'sans-serif',
    'card_bg': '#1a1a1a',
    'success_color': '#2fd36e',
    'warning_color': '#ffd534',
    'danger_color': '#ff4961'
}

# 3D Scatter plot for visual appeal
def create_3d_scatter():
    x = np.random.randn(100)
    y = np.random.randn(100)
    z = np.random.randn(100)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=5,
            color=z,
            colorscale='Viridis',
            opacity=0.8
        )
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(r=0, b=0, l=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_dynamic_dashboard():
    st.title("Hospital Dashboard")
    
    st_autorefresh(interval=10000, key="dashboard_refresh")
    
    current_time = datetime.now()
    times = pd.date_range(end=current_time, periods=20, freq='1min')
    
    # 3D Scatter plot for visual appeal
    st.subheader("Hospital Activity Visualization")
    fig_3d = create_3d_scatter()
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Interactive metrics with hover effect
    col1, col2, col3 = st.columns(3)
    with col1:
        current_patients = np.random.randint(80, 120)
        st.metric("Current Patients", current_patients, delta=np.random.randint(-5, 5))
    with col2:
        bed_capacity = f"{np.random.randint(60, 90)}%"
        st.metric("Bed Capacity", bed_capacity, delta=f"{np.random.randint(-3, 3)}%")
    with col3:
        staff_on_duty = np.random.randint(40, 60)
        st.metric("Staff on Duty", staff_on_duty, delta=np.random.randint(-2, 2))
    
    # Interactive charts
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Patient Flow (Last 20 minutes)", "Department Load (%)"))
    
    # Patient Flow
    fig.add_trace(
        go.Scatter(
            x=times,
            y=np.random.randint(50, 100, size=20),
            name="Admissions",
            mode='lines+markers',
            line=dict(color='#4da6ff', width=3),
            marker=dict(size=8, symbol='circle', line=dict(color='#ffffff', width=2))
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=times,
            y=np.random.randint(40, 90, size=20),
            name="Discharges",
            mode='lines+markers',
            line=dict(color='#ff4961', width=3),
            marker=dict(size=8, symbol='circle', line=dict(color='#ffffff', width=2))
        ),
        row=1, col=1
    )
    
    # Department Load
    departments = ['ER', 'ICU', 'Surgery', 'Pediatrics', 'General']
    values = np.random.randint(40, 100, size=len(departments))
    fig.add_trace(
        go.Bar(
            x=departments,
            y=values,
            marker_color='#4da6ff',
            hoverinfo='y',
            textposition='auto',
            textfont=dict(color='white'),
            hoverlabel=dict(bgcolor='#1a1a1a', font_size=14)
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa'),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    emergency_data = pd.DataFrame({
        'Time': times[-5:],
        'Type': np.random.choice(['Critical', 'Moderate', 'Minor'], size=5),
        'Department': np.random.choice(['ER', 'ICU', 'Surgery'], size=5),
        'Status': np.random.choice(['In Progress', 'Waiting', 'Completed'], size=5)
    })
    
    st.subheader("Recent Emergency Cases")
    st.dataframe(
        emergency_data.style
        .map(lambda x: f'color: {dark_theme["text_color"]}; background-color: {dark_theme["card_bg"]}')
        .set_properties(**{'background-color': dark_theme['card_bg'], 'color': dark_theme['text_color'], 'border-color': dark_theme['primary_color']})
        .highlight_max(axis=0, props='color: #ff4961; font-weight: bold;')
        .highlight_min(axis=0, props='color: #2fd36e; font-weight: bold;'),
        use_container_width=True
    )

def user_profile_section():
    st.title("User Profile")
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'email': '',
            'phone': '',
            'department': '',
            'role': '',
            'profile_picture': None
        }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.user_profile['name'] = st.text_input("Full Name", st.session_state.user_profile['name'])
        st.session_state.user_profile['email'] = st.text_input("Email", st.session_state.user_profile['email'])
        st.session_state.user_profile['phone'] = st.text_input("Phone", st.session_state.user_profile['phone'])
        
    with col2:
        st.session_state.user_profile['department'] = st.selectbox(
            "Department",
            ["Cardiology", "Emergency", "Pediatrics", "Surgery", "Other"],
            index=0 if not st.session_state.user_profile['department'] else None
        )
        st.session_state.user_profile['role'] = st.selectbox(
            "Role",
            ["Doctor", "Nurse", "Administrator", "Other"],
            index=0 if not st.session_state.user_profile['role'] else None
        )
        uploaded_file = st.file_uploader("Upload Profile Picture", type=['jpg', 'png'])
        if uploaded_file is not None:
            st.session_state.user_profile['profile_picture'] = uploaded_file
            st.image(uploaded_file, width=150)
    
    if st.button("Save Profile"):
        st.success("Profile updated successfully!")

def emergency_contact_section():
    st.title("Emergency Contact")
    
    st.header("Emergency Department")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📞 Emergency Hotline\n\n1-800-HOSPITAL")
    with col2:
        st.info("🚑 Ambulance Service\n\n911")
    with col3:
        st.info("👨‍⚕️ On-call Doctor\n\n+1-555-0123")
    
    st.header("Contact Form")
    
    emergency_type = st.selectbox(
        "Emergency Type",
        ["Medical Emergency", "Fire Emergency", "Security Issue", "Other"]
    )
    
    description = st.text_area("Description of Emergency")
    location = st.text_input("Location in Hospital")
    
    if st.button("Submit Emergency Alert"):
        if description and location:
            st.success("Emergency alert submitted successfully!")
            st.info("Emergency response team has been notified.")
        else:
            st.error("Please fill in all required fields.")

def about_us_section():
    st.title("About Us")
    
    st.markdown("""
    ## Our Mission
    To provide exceptional healthcare services with compassion and innovation, 
    ensuring the best possible outcomes for our patients and communities.
    
    ## Our Vision
    To be the leading healthcare provider known for excellence in patient care, 
    medical research, and healthcare technology innovation.
    
    ## Our Values
    - **Excellence** in all aspects of healthcare
    - **Compassion** towards all patients
    - **Innovation** in medical practices
    - **Integrity** in our actions
    - **Teamwork** in our approach
    
    ## Hospital Statistics
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Years of Service", "50+")
    with col2:
        st.metric("Healthcare Professionals", "1000+")
    with col3:
        st.metric("Patients Served Annually", "50,000+")
    
    st.header("Our Departments")
    departments = [
        ("🫀 Cardiology", "Specialized heart care and treatment"),
        ("🧠 Neurology", "Expert neurological care"),
        ("👶 Pediatrics", "Comprehensive children's healthcare"),
        ("🏥 Emergency Care", "24/7 emergency services"),
        ("🔬 Research", "Cutting-edge medical research")
    ]
    
    for dept, desc in departments:
        st.subheader(dept)
        st.write(desc)

def prediction_page():
    st.title("Patient Readmission Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox('Gender:', ["Female", "Male", "Other"])
        admission_type = st.selectbox('Admission Type:', ['Emergency', 'Urgent', 'Elective'])
        diagnosis = st.selectbox('Diagnosis:', ['Heart Disease', 'Diabetes', 'Injury', 'Infection'])
        lab_procedures = st.number_input('Number of Lab Procedures:', 1, 100, 1)
        medications = st.number_input('Number of Medications:', 1, 36, 1)
    
    with col2:
        outpatient_visits = st.number_input('Number of Outpatient Visits:', 0, 5, 0)
        inpatient_visits = st.number_input('Number of Inpatient Visits:', 0, 5, 0)
        emergency_visits = st.number_input('Number of Emergency Visits:', 0, 5, 0)
        num_diagnoses = st.number_input('Number of Diagnoses:', 1, 10, 1)
        a1c_result = st.selectbox('A1C Result:', ['Normal', 'Abnormal'])
    
    if st.button("Predict Readmission", key="predict_button"):
        gender_code = {"Female": 0, "Male": 1, "Other": 2}[gender]
        admission_code = {"Emergency": 1, "Urgent": 2, "Elective": 0}[admission_type]
        diagnosis_code = {"Heart Disease": 1, "Diabetes": 0, "Injury": 3, "Infection": 2}[diagnosis]
        a1c_code = {"Normal": 1, "Abnormal": 0}[a1c_result]
        
        input_data = np.array([[
            gender_code, admission_code, diagnosis_code, lab_procedures,
            medications, outpatient_visits, inpatient_visits,
            emergency_visits, num_diagnoses, a1c_code
        ]])
        
        try:
            model_path = os.path.join(os.path.dirname(__file__), "Readmission_Model.pkl")
            with open(model_path, "rb") as m:
                model = pickle.load(m)
            result = model.predict(input_data)[0]
            
            if result == 1:
                st.error("⚠️ High Risk: Readmission is Required")
                st.markdown("""
                    ### Recommended Actions:
                    1. Schedule follow-up appointment within 7 days
                    2. Review medication compliance
                    3. Coordinate with care management team
                """)
            else:
                st.success("✅ Low Risk: Readmission is Not Required")
                st.markdown("""
                    ### Recommended Actions:
                    1. Schedule routine follow-up within 30 days
                    2. Provide standard discharge instructions
                    3. Document any concerns for future reference
                """)
        except FileNotFoundError:
            st.error("Model file not found. Please ensure 'Readmission_Model.pkl' is in the correct directory.")
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")

def analytics_page():
    st.title("Hospital Analytics Dashboard")
    
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 24 Hours", "Last Week", "Last Month", "Last Year"]
    )
    
    if time_period == "Last 24 Hours":
        dates = pd.date_range(end=datetime.now(), periods=24, freq='h')
    elif time_period == "Last Week":
        dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    elif time_period == "Last Month":
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    else:
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
    
    analytics_data = pd.DataFrame({
        'Date': dates,
        'Admissions': np.random.randint(50, 150, size=len(dates)),
        'Discharges': np.random.randint(40, 140, size=len(dates)),
        'Readmissions': np.random.randint(5, 30, size=len(dates)),
        'Average_Stay': np.random.uniform(2, 7, size=len(dates))
    })
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_admissions = analytics_data['Admissions'].sum()
        st.metric("Total Admissions", f"{total_admissions:,}")
    
    with col2:
        avg_stay = analytics_data['Average_Stay'].mean()
        st.metric("Average Stay (days)", f"{avg_stay:.1f}")
    
    with col3:
        readmission_rate = (analytics_data['Readmissions'].sum() / total_admissions) * 100
        st.metric("Readmission Rate", f"{readmission_rate:.1f}%")
    
    with col4:
        bed_turnover = total_admissions / len(dates)
        st.metric("Daily Bed Turnover", f"{bed_turnover:.1f}")
    
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Admissions vs Discharges Trend", "Readmission Trend", "Average Length of Stay Trend", "Department-wise Statistics"))
    
    # Admissions vs Discharges Trend
    fig.add_trace(go.Scatter(
        x=analytics_data['Date'],
        y=analytics_data['Admissions'],
        name="Admissions",
        line=dict(color='#4da6ff', width=3)
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=analytics_data['Date'],
        y=analytics_data['Discharges'],
        name="Discharges",
        line=dict(color='#ff4961', width=3)
    ), row=1, col=1)
    
    # Readmission Trend
    fig.add_trace(go.Scatter(
        x=analytics_data['Date'],
        y=analytics_data['Readmissions'],
        name="Readmissions",
        line=dict(color='#ffd534', width=3)
    ), row=1, col=2)
    
    # Average Length of Stay Trend
    fig.add_trace(go.Scatter(
        x=analytics_data['Date'],
        y=analytics_data['Average_Stay'],
        name="Average Stay",
        line=dict(color='#2fd36e', width=3)
    ), row=2, col=1)
    
    # Department-wise Statistics
    departments = ['Emergency', 'Surgery', 'Cardiology', 'Pediatrics', 'Neurology']
    occupancy_rates = np.random.uniform(60, 95, len(departments))
    fig.add_trace(go.Bar(
        x=departments,
        y=occupancy_rates,
        name="Occupancy Rate",
        marker_color='#4da6ff'
    ), row=2, col=2)
    
    fig.update_layout(
        height=800,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        )
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Department-wise Statistics")
    dept_data = pd.DataFrame({
        'Department': departments,
        'Occupancy_Rate': occupancy_rates,
        'Avg_Stay': np.random.uniform(2, 8, len(departments)),
        'Patient_Satisfaction': np.random.uniform(75, 95, len(departments))
    })
    
    st.dataframe(
        dept_data.style.format({
            'Occupancy_Rate': '{:.2f}%',
            'Avg_Stay': '{:.2f}',
            'Patient_Satisfaction': '{:.2f}%'
        })
        .map(lambda x: f'color: {dark_theme["text_color"]}; background-color: {dark_theme["card_bg"]}')
        .set_properties(**{'background-color': dark_theme['card_bg'], 'color': dark_theme['text_color'], 'border-color': dark_theme['primary_color']})
        .highlight_max(axis=0, props='color: #2fd36e; font-weight: bold;')
        .highlight_min(axis=0, props='color: #ff4961; font-weight: bold;'),
        use_container_width=True
    )

def medical_image_analysis_page():
    st.title("Medical Image Analysis")
    
    # Disease details dictionary
    DISEASE_DETAILS = {
        'Aortic enlargement': {
            'description': 'Abnormal enlargement of the aorta',
            'precautions': [
                'Immediate cardiovascular consultation',
                'Regular blood pressure monitoring',
                'Avoid heavy lifting and strenuous activities'
            ],
            'admission': 'Immediate hospitalization if risk of rupture'
        },
        'Cardiomegaly': {
            'description': 'Abnormal enlargement of the heart',
            'precautions': [
                'Restrict physical activities',
                'Follow strict medication regimen',
                'Regular cardiac monitoring'
            ],
            'admission': 'Urgent cardiac care if symptoms are severe'
        },
        'Pneumothorax': {
            'description': 'Collapsed or partially collapsed lung',
            'precautions': [
                'Oxygen therapy',
                'Chest tube insertion may be required',
                'Complete bed rest'
            ],
            'admission': 'Immediate hospitalization'
        },
        'No finding': {
            'description': 'No significant medical conditions detected',
            'precautions': ['Regular health check-ups'],
            'admission': 'Not required'
        }
    }
    
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Load YOLO model
    MODEL_PATH = 'yolov8n.pt'
    model = YOLO(MODEL_PATH)
    
    # Disease classes
    CLASSES = [
        'Aortic enlargement', 'Atelectasis', 'Calcification', 'Cardiomegaly',
        'Consolidation', 'ILD', 'Infiltration', 'Lung Opacity', 'Nodule/Mass',
        'Other lesion', 'Pleural effusion', 'Pleural thickening', 'Pneumothorax',
        'Pulmonary fibrosis', 'No finding'
    ]
    
    st.markdown("### Upload Medical Image")
    uploaded_file = st.file_uploader(
        "Choose a medical image (DICOM, JPG, PNG)", 
        type=['dcm', 'dicom', 'jpg', 'png']
    )
    
    if uploaded_file is not None:
        # Save the uploaded file
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        file_path = os.path.join("uploads", uploaded_file.name)
        
        try:
            # Read the image
            if uploaded_file.name.endswith('.dcm') or uploaded_file.name.endswith('.dicom'):
                dicom = pydicom.dcmread(file_path)
                img = dicom.pixel_array
                # Normalize DICOM
                img = (img / img.max() * 255).astype(np.uint8)
                # Convert grayscale DICOM to RGB
                if len(img.shape) == 2:
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            else:
                img = cv2.imread(file_path)
                if img is None:
                    raise ValueError("Could not read image file")
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Perform inference
            results = model(img)
            
            # Process results
            predictions = []
            for r in results:
                boxes = r.boxes.xyxy.cpu().numpy()
                confidences = r.boxes.conf.cpu().numpy()
                class_ids = r.boxes.cls.cpu().numpy().astype(int)
                
                for box, confidence, class_id in zip(boxes, confidences, class_ids):
                    x_min, y_min, x_max, y_max = box
                    predictions.append({
                        'class_name': CLASSES[class_id],
                        'confidence': float(confidence),
                        'box': {
                            'x_min': int(x_min),
                            'y_min': int(y_min),
                            'x_max': int(x_max),
                            'y_max': int(y_max)
                        }
                    })
            
            # If no findings, add a default prediction
            if not predictions:
                predictions.append({
                    'class_name': 'No finding',
                    'confidence': 1.0,
                    'box': {'x_min': 0, 'y_min': 0, 'x_max': 1, 'y_max': 1}
                })
            
            # Visualize results
            visualized_img = img.copy()
            for pred in predictions:
                color = [random.randint(0, 255) for _ in range(3)]
                visualized_img = draw_bbox(visualized_img, 
                                           [pred['box']['x_min'], pred['box']['y_min'], 
                                            pred['box']['x_max'], pred['box']['y_max']],
                                           pred['class_name'], 
                                           pred['confidence'],
                                           color)
            
            st.subheader("Analysis Results")
            
            # Create responsive layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display image responsively
                st.image(visualized_img, use_column_width=True, caption="Analyzed Medical Image")
            
            with col2:
                # Detailed analysis report
                st.markdown("### Detected Conditions")
                
                # Check if predictions exist
                if not predictions:
                    st.info("No significant findings detected.")
                else:
                    for pred in predictions:
                        disease = pred['class_name']
                        confidence = pred['confidence']
                        
                        st.markdown(f"#### {disease}")
                        st.markdown(f"**Confidence:** {confidence:.2%}")
                        
                        # Retrieve disease details
                        if disease in DISEASE_DETAILS:
                            details = DISEASE_DETAILS[disease]
                            st.markdown(f"**Description:** {details['description']}")
                            
                            st.markdown("**Precautions:**")
                            for precaution in details['precautions']:
                                st.markdown(f"- {precaution}")
                            
                            st.markdown(f"**Hospital Admission:** {details['admission']}")
                        
                        st.markdown("---")
            
            # Clean up temporary file
            os.remove(file_path)
        
        except Exception as e:
            st.error(f"An error occurred during image analysis: {str(e)}")

def draw_bbox(image, box, label, confidence, color):   
    alpha = 0.1
    alpha_box = 0.4
    overlay_bbox = image.copy()
    overlay_text = image.copy()
    output = image.copy()

    text_width, text_height = cv2.getTextSize(label.upper(), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
    cv2.rectangle(overlay_bbox, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, -1)
    cv2.addWeighted(overlay_bbox, alpha, output, 1 - alpha, 0, output)
    cv2.rectangle(overlay_text, (int(box[0]), int(box[1])-7-text_height), (int(box[0])+text_width+2, int(box[1])), (0, 0, 0), -1)
    cv2.addWeighted(overlay_text, alpha_box, output, 1 - alpha_box, 0, output)
    cv2.rectangle(output, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
    cv2.putText(output, label.upper(), (int(box[0]), int(box[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(output, f"{confidence:.2f}", (int(box[0]), int(box[3])+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    return output

import google.generativeai as genai
from typing import List
from datetime import datetime
from fpdf import FPDF
import io
import PIL.Image
from gtts import gTTS
import base64

def chatbot_page():
    """AI-powered hospital chatbot using Google Gemini"""
    show_page_header(
        "Hospital AI Assistant",
        "Chat with our AI for medical information and image analysis",
        "💬"
    )
    
    # Medical disclaimer
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(241, 196, 15, 0.1) 0%, rgba(241, 196, 15, 0.05) 100%);
                border-left: 4px solid #F1C40F; border-radius: 12px; padding: 1rem; margin: 1rem 0;">
        <p style="margin: 0; color: #FAFAFA;">
            ⚠️ <strong>Medical Disclaimer:</strong> This chatbot provides general information only. 
            Always consult qualified healthcare professionals for medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for API key
    try:
        api_key = st.secrets["google"]["api_key"]
    except:
        st.error("❌ Google Gemini API key not found!")
        st.info("""
        ### 🔑 How to set up your Google Gemini API key:
        
        1. **Get API Key:**
           - Visit: https://makersuite.google.com/app/apikey
           - Sign in with Google account
           - Click "Create API Key"
        
        2. **Create secrets file:**
           - Create folder: `.streamlit` in your project directory
           - Create file: `secrets.toml` inside `.streamlit` folder
           - Add this content:
           ```toml
           [google]
           api_key = "your-api-key-here"
           ```
        
        3. **Restart** the Streamlit app
        """)
        return
    
    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error configuring Gemini: {str(e)}")
        return
    
    # Settings in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Chat Settings")
        language = st.selectbox(
            "Response Language:",
            ["English", "Hindi", "Marathi"],
            help="Choose the language for AI responses"
        )
        
        model_choice = st.selectbox(
            "AI Model:",
            ["gemini-2.5-flash"],
            help="Gemini 2.5 Flash - Latest AI model from Google"
        )
        
        temperature = st.slider(
            "Creativity Level:",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat cleared!")
            st.rerun()
    
    # Initialize models
    try:
        text_model = genai.GenerativeModel(
            model_choice,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 1000,
            }
        )
        vision_model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Force refresh of chat session to use correct model
    if "gemini_chat" not in st.session_state or "last_model" not in st.session_state or st.session_state.get("last_model") != model_choice:
        st.session_state.gemini_chat = text_model.start_chat(history=[])
        st.session_state.last_model = model_choice
    
    # System prompt for medical context
    system_instruction = f"""You are a helpful hospital AI assistant. Your role is to:
    1. Provide general medical information and hospital services guidance
    2. Answer questions about common medical conditions, symptoms, and treatments
    3. Help patients understand medical terminology
    4. Provide appointment and hospital navigation assistance
    5. Always recommend consulting healthcare professionals for specific medical advice
    
    Respond in {language}. Be empathetic, professional, and clear.
    
    Important: You cannot diagnose conditions or replace professional medical consultation.
    """
    
    # Image upload section
    st.markdown("### 📤 Upload Medical Image (Optional)")
    uploaded_image = st.file_uploader(
        "Upload an image for AI analysis (X-ray, MRI, skin condition, etc.)",
        type=['jpg', 'jpeg', 'png'],
        help="Gemini can analyze medical images and provide insights"
    )
    
    image_for_analysis = None
    if uploaded_image:
        image = PIL.Image.open(uploaded_image)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        with col2:
            st.info("""
            **Image Analysis Available!**
            
            The AI can help identify:
            - General observations
            - Potential abnormalities
            - Recommendations for follow-up
            
            Click "Analyze Image" button below or ask about it in chat.
            """)
        
        image_for_analysis = image
        
        # Quick analyze button
        if st.button("🔍 Analyze This Image Now"):
            with st.spinner("🔍 Analyzing image..."):
                try:
                    prompt = f"Analyze this medical image in detail. Describe what you see, identify any notable features or potential abnormalities, and provide general recommendations. Respond in {language}. Remember this is for educational purposes only and not a medical diagnosis."
                    
                    response = vision_model.generate_content([prompt, image])
                    
                    if response and hasattr(response, "text"):
                        analysis_text = response.text
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": "🖼️ [Image uploaded for analysis]"
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": analysis_text
                        })
                        
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error analyzing image: {str(e)}")
    
    # Display chat history
    st.markdown("### 💬 Chat")
    for idx, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Add TTS option for assistant messages
            if message["role"] == "assistant" and st.button(
                "🔊 Listen", 
                key=f"tts_{idx}"
            ):
                try:
                    lang_code = {'English': 'en', 'Hindi': 'hi', 'Marathi': 'mr'}[language]
                    tts = gTTS(text=message["content"], lang=lang_code)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    audio_base64 = base64.b64encode(audio_buffer.read()).decode()
                    audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
                    st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"TTS not available: {str(e)}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about healthcare, symptoms, or hospital services..."):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Check if user is asking about the uploaded image
                    image_keywords = ["image", "picture", "photo", "scan", "x-ray", "mri", "show", "see"]
                    asking_about_image = any(keyword in prompt.lower() for keyword in image_keywords)
                    
                    # If image is uploaded and user asks about it, use vision model
                    if image_for_analysis and asking_about_image:
                        full_prompt = f"{system_instruction}\n\nUser question: {prompt}\n\nPlease analyze the uploaded medical image and answer the question in {language}."
                        response = vision_model.generate_content([full_prompt, image_for_analysis])
                    else:
                        # Use text model for regular queries
                        full_prompt = f"{system_instruction}\n\n{prompt}"
                        response = st.session_state.gemini_chat.send_message(full_prompt)
                    
                    if response and hasattr(response, "text"):
                        bot_response = response.text
                        
                        # Display and save response
                        st.markdown(bot_response)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": bot_response
                        })
                    else:
                        st.error("❌ No response from AI")
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    
                    if "quota" in str(e).lower() or "resource_exhausted" in str(e).lower():
                        st.warning("⚠️ API quota exceeded. Please wait a minute or check your Gemini account.")
                    elif "api_key" in str(e).lower():
                        st.warning("⚠️ Invalid API key. Please check your secrets.toml file.")
                    elif "blocked" in str(e).lower():
                        st.warning("⚠️ Response was blocked by safety filters. Try rephrasing your question.")
    
    # Export chat option
    if st.session_state.chat_history:
        st.markdown("---")
        with st.expander("📥 Export Chat History"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            txt_content = f"Hospital AI Chat - {timestamp}\n\n"
            for msg in st.session_state.chat_history:
                txt_content += f"{msg['role'].upper()}: {msg['content']}\n\n"
            
            st.download_button(
                "📄 Download as Text File",
                data=txt_content,
                file_name=f"hospital_chat_{timestamp}.txt",
                mime="text/plain"
            )
    
    # Quick suggestions
    st.markdown("---")
    st.markdown("### 💡 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    quick_questions = {
        "🏥 Hospital Services": "What services and departments does the hospital provide?",
        "📅 Appointment Info": "How do I book an appointment at the hospital?",
        "🩺 Common Symptoms": "What are common symptoms I should watch for and when should I see a doctor?"
    }
    
    with col1:
        if st.button("🏥 Hospital Services"):
            st.session_state.quick_question = quick_questions["🏥 Hospital Services"]
            st.rerun()
    with col2:
        if st.button("📅 Appointment Info"):
            st.session_state.quick_question = quick_questions["📅 Appointment Info"]
            st.rerun()
    with col3:
        if st.button("🩺 Common Symptoms"):
            st.session_state.quick_question = quick_questions["🩺 Common Symptoms"]
            st.rerun()
    
    # Handle quick questions
    if "quick_question" in st.session_state and st.session_state.quick_question:
        # Process the quick question
        st.session_state.chat_history.append({
            "role": "user",
            "content": st.session_state.quick_question
        })
        
        try:
            response = st.session_state.gemini_chat.send_message(
                f"{system_instruction}\n\n{st.session_state.quick_question}"
            )
            if response and hasattr(response, "text"):
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response.text
                })
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.session_state.quick_question = None
        st.rerun()



    st.markdown("---")
    st.markdown("Made with ❤️ for Tatva-AI")
# Add chatbot to main navigation
import tensorflow as tf
from PIL import Image

# Add this function after the medical_image_analysis_page() function
def brain_tumor_detection_page():
    """Enhanced brain tumor detection with visual localization"""
    show_page_header(
        "Brain Tumor Detection", 
        "AI-powered tumor classification with visual detection",
        "🧠"
    )
    
    def load_model_with_custom_objects(model_path):
        def custom_depthwise_conv2d(*args, **kwargs):
            if 'groups' in kwargs:
                del kwargs['groups']
            return tf.keras.layers.DepthwiseConv2D(*args, **kwargs)
        
        custom_objects = {
            'DepthwiseConv2D': custom_depthwise_conv2d,
            'tf': tf
        }
        
        try:
            model = tf.keras.models.load_model(
                model_path, 
                custom_objects=custom_objects,
                compile=False
            )
            return model
        except Exception as e:
            st.error(f"Model loading failed: {e}")
            return None

    def preprocess_image(image):
        """Preprocess image for model input"""
        image = image.convert("RGB")
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array

    def get_gradcam_heatmap(model, img_array, pred_index=None):
        """Generate GradCAM heatmap for tumor localization"""
        try:
            # Get the last convolutional layer
            last_conv_layer = None
            for layer in reversed(model.layers):
                if len(layer.output_shape) == 4:  # Conv layer
                    last_conv_layer = layer
                    break
            
            if last_conv_layer is None:
                return None
            
            # Create a model that maps the input to the last conv layer and predictions
            grad_model = tf.keras.models.Model(
                [model.inputs],
                [last_conv_layer.output, model.output]
            )
            
            # Compute gradient
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                if pred_index is None:
                    pred_index = tf.argmax(predictions[0])
                class_channel = predictions[:, pred_index]
            
            # Get gradients
            grads = tape.gradient(class_channel, conv_outputs)
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Weight the channels by importance
            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            
            # Normalize heatmap
            heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
            return heatmap.numpy()
            
        except Exception as e:
            st.warning(f"GradCAM visualization unavailable: {str(e)}")
            return None

    def draw_tumor_detection(original_image, heatmap, threshold=0.5):
        """Draw red bounding box around detected tumor region"""
        # Convert PIL to numpy array first
        img_array = np.array(original_image)
        
        # Ensure it's RGB format
        if len(img_array.shape) == 2:  # Grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # Now convert RGB to BGR for OpenCV
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        height, width = img_cv.shape[:2]
        
        if heatmap is not None:
            # Resize heatmap to match image size
            heatmap_resized = cv2.resize(heatmap, (width, height))
            
            # Threshold the heatmap to find tumor regions
            _, binary_mask = cv2.threshold(
                (heatmap_resized * 255).astype(np.uint8), 
                int(threshold * 255), 
                255, 
                cv2.THRESH_BINARY
            )
            
            # Find contours of tumor regions
            contours, _ = cv2.findContours(
                binary_mask, 
                cv2.RETR_EXTERNAL, 
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Draw bounding boxes on detected regions
            if len(contours) > 0:
                # Find the largest contour (main tumor region)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Only draw if area is significant (avoid noise)
                if w * h > (width * height * 0.01):  # At least 1% of image
                    # Draw red bounding box
                    cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    
                    # Add label
                    label = "TUMOR DETECTED"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.7
                    thickness = 2
                    
                    # Get text size for background
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label, font, font_scale, thickness
                    )
                    
                    # Draw background rectangle for text
                    cv2.rectangle(
                        img_cv, 
                        (x, y - text_height - 10), 
                        (x + text_width, y), 
                        (0, 0, 255), 
                        -1
                    )
                    
                    # Draw text
                    cv2.putText(
                        img_cv, 
                        label, 
                        (x, y - 5), 
                        font, 
                        font_scale, 
                        (255, 255, 255), 
                        thickness
                    )
                    
                    # Create heatmap overlay
                    heatmap_colored = cv2.applyColorMap(
                        (heatmap_resized * 255).astype(np.uint8), 
                        cv2.COLORMAP_JET
                    )
                    overlay = cv2.addWeighted(img_cv, 0.6, heatmap_colored, 0.4, 0)
                    
                    return cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB), cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        
        # Return original if no detection
        return cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB), None

    # Main page content
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(231, 76, 60, 0.05) 100%);
                border-left: 4px solid #E74C3C; border-radius: 12px; padding: 1rem; margin: 1rem 0;">
        <p style="margin: 0; color: #FAFAFA;">
            ⚠️ <strong>Medical Disclaimer:</strong> This AI tool is for educational purposes only. 
            Always consult qualified healthcare professionals for medical diagnosis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    model_path = 'models/keras_model.h5'
    model = load_model_with_custom_objects(model_path)
    
    if model is None:
        st.error("❌ Could not load the brain tumor detection model.")
        return
    
    st.success("✅ Model loaded successfully!")
    
    # File uploader with instructions
    st.markdown("### 📤 Upload Brain Scan Image")
    uploaded_file = st.file_uploader(
        "Choose a brain MRI scan (JPG, PNG, or JPEG format)", 
        type=['jpg', 'png', 'jpeg'],
        help="Upload a clear brain MRI scan image for tumor detection"
    )
    
    # Advanced settings in expander
    with st.expander("⚙️ Advanced Settings"):
        detection_threshold = st.slider(
            "Detection Sensitivity",
            min_value=0.3,
            max_value=0.8,
            value=0.5,
            step=0.05,
            help="Higher values = more precise detection, Lower values = more sensitive"
        )
        show_heatmap = st.checkbox("Show Heatmap Overlay", value=True)
    
    if uploaded_file is not None:
        with st.spinner("🔍 Analyzing brain scan..."):
            # Load and display original image
            image = Image.open(uploaded_file)
            
            try:
                # Preprocess for model
                processed_image = preprocess_image(image)
                
                # Get predictions
                predictions = model.predict(processed_image, verbose=0)
                
                CLASS_LABELS = ["Pituitary", "No Tumor", "Meningioma", "Glioma"]
                predicted_idx = np.argmax(predictions[0])
                predicted_class = CLASS_LABELS[predicted_idx]
                confidence = predictions[0][predicted_idx]
                
                # Generate GradCAM heatmap
                heatmap = None
                if predicted_class != "No Tumor":
                    heatmap = get_gradcam_heatmap(model, processed_image, predicted_idx)
                
                # Draw detection boxes
                annotated_image, heatmap_overlay = draw_tumor_detection(
                    image, 
                    heatmap, 
                    threshold=detection_threshold
                )
                
                # Display results in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📷 Original Scan")
                    st.image(image, use_column_width=True)
                
                with col2:
                    if predicted_class != "No Tumor" and heatmap is not None:
                        st.markdown("#### 🎯 Detection Result")
                        st.image(annotated_image, use_column_width=True)
                    else:
                        st.markdown("#### ✅ Clean Scan")
                        st.image(image, use_column_width=True)
                        st.info("No tumor detected in this scan")
                
                # Show heatmap overlay if enabled
                if show_heatmap and heatmap_overlay is not None and predicted_class != "No Tumor":
                    st.markdown("#### 🔥 Attention Heatmap")
                    st.image(heatmap_overlay, use_column_width=True, 
                            caption="Red areas show where the AI focused attention")
                
                # Results section
                st.markdown("---")
                st.markdown("### 📊 Analysis Results")
                
                # Main prediction with color coding
                if predicted_class == "No Tumor":
                    st.success(f"✅ **Diagnosis:** {predicted_class}")
                else:
                    st.error(f"⚠️ **Diagnosis:** {predicted_class} Detected")
                
                st.metric(
                    "Confidence Level", 
                    f"{confidence*100:.2f}%",
                    help="How confident the AI is in this prediction"
                )
                
                # Detailed probabilities
                st.markdown("#### 📈 Detailed Classification Probabilities")
                
                # Create columns for progress bars
                for label, prob in zip(CLASS_LABELS, predictions[0]):
                    col_label, col_bar, col_percent = st.columns([1, 3, 1])
                    with col_label:
                        st.write(f"**{label}:**")
                    with col_bar:
                        st.progress(float(prob))
                    with col_percent:
                        st.write(f"{prob*100:.2f}%")
                
                # Recommendations based on result
                st.markdown("---")
                st.markdown("### 💡 Recommendations")
                
                if predicted_class == "No Tumor":
                    create_info_card(
                        "Normal Scan",
                        "No abnormalities detected. Continue routine health monitoring.",
                        "#27AE60"
                    )
                else:
                    create_info_card(
                        "Professional Consultation Required",
                        f"{predicted_class} tumor detected. Immediate consultation with a neurologist or neurosurgeon is strongly recommended for proper diagnosis and treatment planning.",
                        "#E74C3C"
                    )
                    
                    st.markdown("**Next Steps:**")
                    st.markdown("""
                    1. 🏥 Schedule appointment with neurosurgeon
                    2. 📋 Get comprehensive MRI with contrast
                    3. 🧪 Consider biopsy for confirmation
                    4. 📊 Discuss treatment options
                    """)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.exception(e)




def main():
    # ============================================
    # PAGE CONFIGURATION
    # ============================================
    st.set_page_config(
        page_title="Tatva AI - Hospital Management",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/PIYUSH-JOSHI1/Readmission-Prediction',
            'Report a bug': "https://github.com/PIYUSH-JOSHI1/Readmission-Prediction/issues",
            'About': "# Tatva AI Hospital Management System\nAdvanced healthcare management with AI-powered diagnostics."
        }
    )
    
    # Load custom CSS
    load_custom_css()
    
    # ============================================
    # SESSION STATE INITIALIZATION
    # ============================================
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    languages = load_languages()
    
    # ============================================
    # SIDEBAR NAVIGATION
    # ============================================
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div class="logo-container">
            <h2 style='color: #2E86DE; font-weight: 800; text-align: center; margin-bottom: 0;'>
                🏥 Tatva AI
            </h2>
            <p style='color: #B8BCC8; text-align: center; font-size: 0.9rem; margin-top: 0.5rem;'>
                Advanced Healthcare Management
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display logo if exists
        if os.path.exists("logo.jpeg"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("logo.jpeg", width=120)
        
        st.markdown("---")
        
        # User profile display
        if 'user_profile' in st.session_state and st.session_state.user_profile.get('name'):
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <p style="color: #B8BCC8; margin: 0;">Welcome back,</p>
                <p style="color: #2E86DE; font-weight: 600; font-size: 1.1rem; margin: 0.25rem 0;">
                    {st.session_state.user_profile['name']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.user_profile.get('profile_picture'):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(st.session_state.user_profile['profile_picture'], width=80)
            
            st.markdown("---")
        
        # Navigation menu
        st.markdown("### 📋 Navigation")
        menu_options = [
            "Dashboard", 
            "Patient Prediction", 
            "Analytics", 
            "Brain Tumor Detection",
            "Medical Image Analysis",
            "User Profile", 
            "Emergency Contact", 
            "About Us", 
            "Settings",
            "Chatbot" 
        ]
        
        # Create cleaner selectbox
        selected_page = st.selectbox(
            "Choose a section:",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick stats in sidebar
        st.markdown("### 📈 System Status")
        st.metric("Active Users", "1,234", "+56")
        st.metric("System Health", "98%", "+2%")
        
        st.markdown("---")
        
        # Footer in sidebar
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #6C7A89; font-size: 0.8rem;">
            <p style="margin: 0;">© 2026 Tatva AI</p>
            <p style="margin: 0.25rem 0 0 0;">Version 2.0</p>
        </div>
        """, unsafe_allow_html=True)
    

    
     
    if selected_page == "Chatbot":
        chatbot_page()
    # Page rendering based on selection
    if selected_page == "Dashboard":
        create_dynamic_dashboard()
    elif selected_page == "Patient Prediction":
        prediction_page()
    elif selected_page == "Brain Tumor Detection":
        brain_tumor_detection_page()
    elif selected_page == "Analytics":
        analytics_page()
    elif selected_page == "Medical Image Analysis":
        medical_image_analysis_page()
    elif selected_page == "User Profile":
        user_profile_section()
    elif selected_page == "Emergency Contact":
        emergency_contact_section()
    elif selected_page == "About Us":
        about_us_section()
    elif selected_page == "Settings":
        st.title("Settings")
        
        st.subheader("Language Settings")
        new_language = st.selectbox(
            "Select Language",
            list(languages.keys()),
            index=list(languages.keys()).index(st.session_state.language)
        )
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.experimental_rerun()
        
        st.subheader("Theme Settings")
        theme = st.selectbox(
            "Choose Theme",
            ["Dark"]
        )
        
        current_theme = dark_theme
        st.markdown(f"""
            <style>
            :root {{
                --primary-color: {current_theme['primary_color']};
                --background-color: {current_theme['background_color']};
                --secondary-bg: {current_theme['secondary_bg']};
                --text-color: {current_theme['text_color']};
                --font: {current_theme['font']};
                --card-bg: {current_theme['card_bg']};
                --success-color: {current_theme['success_color']};
                --warning-color: {current_theme['warning_color']};
                --danger-color: {current_theme['danger_color']};
            }}
            </style>
        """, unsafe_allow_html=True)

    # Add 3D effect and continuous movement
    st.markdown("""
    <script>
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        const elements = document.querySelectorAll('.stPlotlyChart, .stDataFrame, .stMetric');
        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            el.style.transform = `perspective(1000px) rotateY(${x * 5}deg) rotateX(${-y * 5}deg)`;
        });
    });
    </script>
    <style>
    .custom-cursor {
        width: 20px;
        height: 20px;
        border: 2px solid #ffffff;
        border-radius: 50%;
        position: fixed;
        pointer-events: none;
        z-index: 9999;
        mix-blend-mode: difference;
    }
    .stPlotlyChart, .stDataFrame, .stMetric {
        transition: transform 0.1s ease;
    }
    .stMetric {
        background: linear-gradient(145deg, rgba(26,26,26,0.6) 0%, rgba(26,26,26,0.8) 100%);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        background: linear-gradient(145deg, rgba(26,26,26,0.8) 0%, rgba(26,26,26,1) 100%);
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
