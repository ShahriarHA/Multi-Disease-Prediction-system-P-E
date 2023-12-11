import pickle
import streamlit as st
# from streamlit_option_menu import option_menu

import torchvision
from PIL import Image
import torch
from torchvision import transforms


# loading the saved pretrained model
Pneumonia_model = pickle.load(open('D:/NEUB/MachineLearning/Stramlit_ Project/multi_disease_prediction/saved_models/pneumonia-disease-pretrained-mode.sav','rb'))

eye_disease_model = pickle.load(open('D:/NEUB/MachineLearning/Stramlit_ Project/multi_disease_prediction/saved_models/eye-disease-pretrained-mode.sav','rb'))

# models prediction function
# pneumonia prediction
def predict_pneumonia(image_path, model):
    individual_image_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomGrayscale(p=1),
        transforms.ToTensor(),
        transforms.Normalize([0.0020], [0.0010])
    ])

    individual_image = Image.open(image_path).convert("RGB")
    individual_image = individual_image_transform(individual_image)
    individual_image = individual_image.unsqueeze(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    individual_image = individual_image.to(device)
    model.eval()

    with torch.no_grad():
        output = model(individual_image)

    _, predicted_class = torch.max(output, 1)
    predicted_class = predicted_class.item()

    return predicted_class

# eye-disease prediction using transfer learning
def predict_eye_disease_tf(image_path, model):
    individual_image_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.0014, 0.0012, 0.0007], [0.0007, 0.0006, 0.0004])
    ])

    individual_image = Image.open(image_path)

    individual_image = individual_image_transform(individual_image)
    individual_image = individual_image.unsqueeze(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    pre_trained_moedl = model.to(device)
    individual_image = individual_image.to(device)

    pre_trained_moedl.eval()
    with torch.no_grad():
        output = pre_trained_moedl(individual_image)
    
    _,predicted_class = torch.max(output, 1)
    predicted_class = predicted_class.item()

    return predicted_class


# Placeholder models
def load_pneumonia_cnn_model():
    st.write("# Pneumonia CNN Model Code\n# Your CNN code here")
    # Load your CNN model and perform predictions

def load_pneumonia_transfer_learning_model():
    st.write("##### Transfer Learning Model useses DenseNet161 pretrained model")
    # Load your transfer learning model and perform predictions
    chest_x_ray_image = st.file_uploader('Please uploade your chest x-ray image',type=['jpeg','png','jpg'])
    if chest_x_ray_image is not None:
        st.image(chest_x_ray_image, caption='Uploaded Image.')
        # Predict the class
        predicted_class = predict_pneumonia(chest_x_ray_image, Pneumonia_model)
        if predicted_class == 0:
            st.success("The image is predicted as Normal.")
        elif predicted_class == 1:
            st.error("The image is predicted as Pneumonia.")
        else:
            st.warning("Unable to determine the prediction.")
    else:
        st.warning('Please upload a chest x-ray image.')

def load_pneumonia_naive_bayes_model():
    st.write("# Pneumonia Naive Bayes Model Code\n# Your Naive Bayes code here")
    # Load your naive bayes model and perform predictions

def load_eye_disease_cnn_model():
    st.write("# Eye Disease CNN Model Code\n# Your CNN code here")
    # Load your CNN model and perform predictions

def load_eye_disease_transfer_learning_model():
    st.write("##### Transfer Learning Model useses DenseNet161 pretrained model")
    # Load your transfer learning model and perform predictions
    eye_disease_image = st.file_uploader('Please uploade your eye-disease image',type=['jpeg','png','jpg'])
    if eye_disease_image is not None:
        st.image(eye_disease_image,caption='Uploaded image')

        predicted_class = predict_eye_disease_tf(eye_disease_image,eye_disease_model)
        if(predicted_class == 0):
            st.error("The image is predicted as Cataract.")
        elif(predicted_class == 1):
            st.error("The image is predicted as Diabetic Retinopethy.")
        elif(predicted_class == 2):
            st.error("The image is predicted as Glaucoma.")
        elif(predicted_class == 3):
            st.success('The image is predicted as Normal.')
        else:
            st.warning("Unable to determine the prediction.")
        
    else:
        st.warning('Please upload a eye-disease image.')



def load_eye_disease_naive_bayes_model():
    st.write("# Eye Disease Naive Bayes Model Code\n# Your Naive Bayes code here")
    # Load your naive bayes model and perform predictions

# navigation bar
selected_disease = st.sidebar.selectbox('Select Disease', ['Pneumonia', 'Eye disease'])

# Load models based on disease selection
if selected_disease == 'Pneumonia':
    selected_model = st.sidebar.selectbox('Select Model', ['CNN', 'Transfer Learning', 'Naive Bayes'])
    st.subheader(f'{selected_disease} - {selected_model} Prediction Page')

    if selected_model == 'CNN':
        load_pneumonia_cnn_model()
    elif selected_model == 'Transfer Learning':
        load_pneumonia_transfer_learning_model()
    elif selected_model == 'Naive Bayes':
        load_pneumonia_naive_bayes_model()

elif selected_disease == 'Eye disease':
    selected_model = st.sidebar.selectbox('Select Model', ['CNN', 'Transfer Learning', 'Naive Bayes'])
    st.subheader(f'{selected_disease} - {selected_model} Prediction Page')

    if selected_model == 'CNN':
        load_eye_disease_cnn_model()
    elif selected_model == 'Transfer Learning':
        load_eye_disease_transfer_learning_model()
    elif selected_model == 'Naive Bayes':
        load_eye_disease_naive_bayes_model()



