# Planejamento:

# titulo
# input do chat
# a cada mensagem enviada:
    # mostrar a mensagem que o usuario enviou no chat
    # enviar essa mensagem para a IA responder
    # aparece na tela a resposta da IA

# Streamlit - apenas usando o python para o frontend e o backend

# Importa a biblioteca Streamlit para criar a interface web
import streamlit as st

#Importa a biblioteca da API do Google Gemini
import google.generativeai as genai

# Configura a chave da API do Google Gemini
genai.configure(api_key="AIzaSyDtHC8ZyccpD8tbX8rTOc45eWBGfRedl3U")

modelo_ia = genai.GenerativeModel("models/gemini-2.5-flash")

st.write("# Chatbot com PY")

# Verifica se já existe um histórico de mensagens salvo na sessão
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = []

texto_usuario = st.chat_input("Digite sua mensagem")

# Exibe todas as mensagens anteriores armazenadas na sessão
for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]  # identifica se é usuário ou assistente
    content = mensagem["content"] # conteúdo da mensagem
    st.chat_message(role).write(content)


# Verifica se o usuário digitou alguma mensagem
if texto_usuario:
    st.chat_message("user").write(texto_usuario) # Mostra a mensagem do usuário na tela
    mensagem_usuario = {"role": "user", "content": texto_usuario} # Dicionário contendo as informações
    st.session_state["lista_mensagens"].append(mensagem_usuario) #  # Adiciona a mensagem do usuário no histórico de mensagens

    # Resposta da ia
    historico = ""

# Percorre todas as mensagens salvas na sessão
# e monta uma string com o histórico completo
    for m in st.session_state["lista_mensagens"]:
        historico += f"{m['role']}: {m['content']}\n"

    ia_resposta = modelo_ia.generate_content(historico)  # Envia o histórico da conversa para o modelo de IA gerar uma resposta

    if ia_resposta.candidates: # Verifica se a IA conseguiu gerar uma resposta
        texto_resposta_ia = ia_resposta.candidates[0].content.parts[0].text  # Extrai o texto da resposta gerada pela IA
    else:
        texto_resposta_ia = "Não consegui gerar uma resposta."  # Caso não tenha resposta disponível

    st.chat_message("assistant").write(texto_resposta_ia)  # Mostra a resposta da IA na interface do chat
    mensagem_ia = {"role": "assistant", "content": texto_resposta_ia}   # Cria um dicionário com a resposta da IA
    st.session_state["lista_mensagens"].append(mensagem_ia)  # Salva a resposta da IA no histórico de mensagens

    print(st.session_state["lista_mensagens"])