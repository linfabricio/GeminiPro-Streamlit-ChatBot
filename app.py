import os
import streamlit as st
import google.generativeai as genai

try:
    gemini_api_key = "AIzaSyC-olCwIDRdlJOC5h3CwTQyD1t9Pfz2VGo"
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Definir el mensaje de sistema para la configuración inicial
    system_message = "Hola! Soy gemini, tu administrador de biblioteca. Mi tarea principal es recomendar libros a los usuarios según la categoría que soliciten. Puedo recomendar libros de diferentes géneros y dar una breve descripción de cada uno."

    if "chat" not in st.session_state:
        # Establecer el contexto inicial del chat
        context = [
            {
                "role" : "model",
                "parts" : [
                    {
                        "text" : system_message
                    }
                ],
            }
        ]
        st.session_state.chat = model.start_chat(history=context)
    
    st.title('Gemini Admin Biblioteca')

    # Crear tres columnas para los botones
    col1, col2, col3 = st.columns(3)
    
    # Colocar un botón en cada columna
    with col1:
        if st.button("Iniciar Chat"):
            st.write("Chat iniciado...")
    with col2:
        if st.button("Actualizar"):
            st.write("Contenido actualizado.")
    with col3:
        if st.button("Ayuda"):
            st.write("Información de ayuda.")

    def role_to_streamlit(role: str) -> str:
      if role == 'model':
        return 'assistant'
      else:
        return role

    for message in st.session_state.chat.history:
      with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

    # Manejo de la entrada del usuario
    if prompt := st.chat_input("Escriba la categoria del libro"):
        # Mostrar el mensaje del usuario en la interfaz
        st.chat_message("user").markdown(prompt)
        
        # Enviar el mensaje del usuario al modelo y recibir la respuesta
        response = st.session_state.chat.send_message(prompt)
        
        # Mostrar la respuesta del asistente en la interfaz
        with st.chat_message("assistant"):
            st.markdown(response.text)

except Exception as e:
    st.error(f'An error occurred: {e}')
