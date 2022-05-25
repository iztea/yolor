from yolor import *
import cv2
import tempfile
import streamlit as st

def main():
    st.title('Object Detection Dashboard')

    st.sidebar.title('Settings')

    st.markdown("""
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width: 480px;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{width: 480px; margin-left: -400px}
    </style>
    """,
    unsafe_allow_html=True,)

    st.sidebar.markdown('---')
    confidence = st.sidebar.slider('Confidence', min_value = 0.0, max_value=1.0, value=0.3)
    st.sidebar.markdown('---')
   
    save_img = st.sidebar.checkbox('Save Video')
    enable_GPU = st.sidebar.checkbox('Enable GPU (Khusus Pengguna GPU')
    custom_classes = st.sidebar.checkbox('Use Custom Classes')
    assigned_class_id = []

    ##Custom Class
    if custom_classes:
        assigned_class = st.sidebar.multiselect('Select Custom Classes', list(names), default='car')
        for each in assigned_class:
            assigned_class_id.append(names.index(each))
    
    ##Upload FIle
    video_file_buffer = st.sidebar.file_uploader("Upload Video", type= ["mp4", "mov", "avi"])
    DEMO_VIDEO = 'demo.mp4'
    tfflie = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)

    if not video_file_buffer:
        vid = cv2.VideoCapture(DEMO_VIDEO)
        tfflie.name = DEMO_VIDEO
        dem_vid = open(tfflie.name, 'rb')
        demo_bytes = dem_vid.read()

        st.sidebar.text('Masukkan Video')
        st.sidebar.video(demo_bytes)

    else:
        tfflie.write(video_file_buffer.read())
        dem_vid = open(tfflie.name, 'rb')
        demo_bytes = dem_vid.read()

        st.sidebar.text('Masukkan Video')
        st.sidebar.video(demo_bytes)
    

    print(tfflie.name)

    stframe = st.empty()
    st.sidebar.markdown('---')

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown("**Frame Rate**")
        kpi1_text = st.markdown("0")
    with kpi2:
        st.markdown("**Object Terdeteksi**")
        kpi2_text = st.markdown("0")
    with kpi3:
        st.markdown("**Lebar**")
        kpi3_text = st.markdown("0")
    
    load_yolor_and_process_each_frame(tfflie.name, enable_GPU, confidence, assigned_class_id, kpi1_text, kpi2_text, kpi3_text, stframe)
    
    st.text(' Video Diproses')
    vid.release()

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass