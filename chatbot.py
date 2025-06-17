import streamlit as st
import groq
#para iniciar la pagina poner "streamlit run chatbot.py" en la terminal
# TENER NUESTRO MODELOS IA
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768','gemma2-9b-it'] # INDICES

# configurar la pagina
def configurar_pagina():
    st.set_page_config(page_title="MI PRIMERA PAGINA", page_icon="👉") #cambia el nombre de la ventana del navegador
    st.title("Bienvenidos a mi chatbot :D") #Es un titulo    

#MOSTRAR UN SIDEBAR CON LOS MODELOS IA
def mostrar_sidebar():
    st.sidebar.title("ELEGI TU MODELO DE IA")
    modelo = st.sidebar.selectbox("**¿Que modelo usaras?**", MODELOS, index=0) #el index sirve oara elegir indice un predeterminado en tu barra
    st.write(f"**Elegiste el modelo:** {modelo}")
    return modelo

# UN CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"] #almacenar la api key de groq
    return groq.Groq(api_key=groq_api_key)

#INICIALIZAR EL ESTADO DE LOS MENSAJES
def inicializacion_estado_chat ():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #lista
#muestra mensajes previos

#Historial del chat 
def mostrar_historial ():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]): #quien lo envia
            st.markdown(mensaje["content"]) #que envia

#Obtener mensaje de usuario
def obtener_mensaje ():
    return st.chat_input("Envia un mensaje")

#Agregar los mensajes al estado
def agregar_mensaje_historial (role,content):
    st.session_state.mensajes.append({"role":role,"content":content})

#Mostrar los mensajes en pantalla
def mostrar_mensaje (role,content):
    with st.chat_message(role):
        st.markdown (content)
    
# LLAMAR AL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content

def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()
    inicializacion_estado_chat()
    mostrar_historial()
    mensaje_usuario = obtener_mensaje()
    if mensaje_usuario:
        agregar_mensaje_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensaje_historial("assistant", respuesta)
        mostrar_mensaje("assistant", respuesta)

    
if __name__ == '__main__':  #si este archivo es el archivo principal, entonces EJECUTA
    ejecutar_app()
    
#--------------------------------------------------------