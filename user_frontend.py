# user_frontend.py
# [Isi lengkap GUI pengguna dengan login wajah, registrasi, top-up]
import streamlit as st
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import user_db
import bcrypt

detector = MTCNN()
model = load_model("facenet_keras.h5")

st.title("💳 FacePay - Sistem Pembayaran Wajah")

menu = st.sidebar.selectbox("Menu", ["Registrasi", "Top Up", "Bayar"])

def capture_image():
    cap = cv2.VideoCapture(0)
    st.info("Tekan 'q' untuk capture")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return frame

def extract_face(img):
    faces = detector.detect_faces(img)
    if faces:
        x, y, w, h = faces[0]['box']
        return cv2.resize(img[y:y+h, x:x+w], (160, 160))
    return None

def get_embedding(face):
    face = face.astype("float32") / 255.0
    return model.predict(np.expand_dims(face, axis=0))[0]

if menu == "Registrasi":
    name = st.text_input("Nama Lengkap")
    pin = st.text_input("PIN (6 digit)", type="password")
    if st.button("Capture & Daftar"):
        if len(pin) == 6 and pin.isdigit():
            img = capture_image()
            face = extract_face(img)
            if face is not None:
                emb = get_embedding(face)
                user_db.register_user(name, emb, pin, img)
                st.success("Registrasi berhasil!")
            else:
                st.error("Wajah tidak terdeteksi!")
        else:
            st.warning("PIN harus 6 digit angka!")

elif menu == "Top Up":
    name = st.text_input("Nama")
    amount = st.number_input("Nominal Top Up", min_value=0)
    if st.button("Top Up"):
        user_db.topup_saldo(name, amount)
        st.success("Saldo ditambahkan")

elif menu == "Bayar":
    st.info("Arahkan wajah ke kamera")
    img = capture_image()
    face = extract_face(img)
    if face is not None:
        emb = get_embedding(face)
        nama, jarak = user_db.identify_user(emb)
        if nama:
            st.success(f"Terdeteksi: {nama} (jarak: {jarak:.2f})")
            if st.button("Bayar"):
                success = user_db.process_payment(nama)
                if success:
                    st.success("Pembayaran berhasil!")
                else:
                    st.error("Saldo tidak cukup")
        else:
            st.warning("Tidak dikenali. Gunakan PIN fallback.")
            pin_name = st.text_input("Masukkan nama")
            pin_code = st.text_input("PIN", type="password")
            if st.button("Verifikasi PIN"):
                result = user_db.validate_pin(pin_name, pin_code)
                if result == "valid":
                    user_db.process_payment(pin_name)
                    st.success("Pembayaran via PIN berhasil")
                elif result == "locked":
                    st.error("PIN dikunci. Hubungi admin.")
                else:
                    st.warning("PIN salah!")
    else:
        st.error("Wajah tidak terdeteksi")
