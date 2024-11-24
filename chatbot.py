import streamlit as st
from groq import Groq

#Agregando el nombre a mi pestaña
st.set_page_config(page_title="Mi chatbot con IA" , page_icon="🐼")

#Titulo de la aplicacion
st.title("Mi primera aplicacion con Streamlit / IA")

#Input para entrada de texto 
nombre = st.text_input("Ingrese su nombre")

#Boton para mostrar un saludo
if st.button("Saludar"):
    st.write(f'Hola {nombre}, Bienvenido/a a mi chatbot')

# modelos = ["modelo 1", "modelo 2", "modelo 3"] #Clase 6
modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
def configurar_pagina():
    #Agregar titulo principal a nuestra barra lateral
    st.title("Mi modelo de chatbot con IA")
    st.sidebar.title("Configuración")
    elegirModelo = st.sidebar.selectbox("Elegir un modelo", options= modelos, index=0)
    return elegirModelo

def crear_usuario_groq():
    claveSecreta = st.secrets['CLAVE_API']
    return Groq(api_key=claveSecreta)

def configurar_modelo(cliente,modelo,mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages = [{"role":"user", "content":mensajeDeEntrada}],
        stream=True  #hace dar una apariencia que esta escribiendo en tiempo real la respuesta
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #guarda msj es un historial

def actualizar_historial(rol,contenido,avatar):
    st.session_state.mensajes.append({"role":rol, "content":contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]):
            st.markdown(mensaje["content"])
def area_chat():
    contenedorDelChat= st.container(height= 400, border= True)
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa=""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return generar_respuesta

def main():
    modelo = configurar_pagina()
    clienteUsuario= crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje= st.chat_input("Escribi tu msj")
    if mensaje:
        actualizar_historial("user", mensaje, "😎")
        chat_completo= configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa= st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"😀")
                
                st.rerun()
if __name__ =="__main__":
    main()
