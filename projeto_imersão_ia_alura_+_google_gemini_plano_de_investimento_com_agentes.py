
"""Projeto Imersão IA Alura + Google Gemini - Plano de Investimento com Agentes
"""
!pip install -q google-adk

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types 
from datetime import date
import textwrap
from IPython.display import display, Markdown 
import requests
import warnings

warnings.filterwarnings("ignore")

def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()

    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Agente 1: Diagnóstico financeiro
def agente_diagnostico(dados_cliente):

    diagnostico = Agent(
        name="agente_diagnostico",
        model="gemini-2.0-flash",
        instruction="""
         Você é um especialista financeiro. Seu trabalho é analisar a situação atual do cliente, considerando:
        - Patrimônio investido
        - Dividendos mensais recebidos
        - Valor dos aportes mensais
        - Rentabilidade média esperada
        Com base nisso, faça uma simulação de em quantos anos ele poderá atingir R$ 1 milhão em patrimônio, considerando juros compostos.
        Mostre cenários otimista, realista e conservador.
        """,
        description="Agente que coleta os fundamentos mais relevantes",
        tools=[google_search]
    )

    entrada = f"Dados do cliente: {dados_cliente}"
    resultado = call_agent(diagnostico, entrada)
    return resultado

# Agente 2: Otimizador de Investimentos
def agente_otimizador(carteira_atual):
    otimizador = Agent(
        name="agente_otimizador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um analista de investimentos. Sua função é avaliar a carteira atual do cliente e sugerir melhorias:
        - Rebalancear entre ações, renda fixa e fundos
        - Reduzir risco (se necessário) ou aumentar retorno potencial
        - Considerar perfil de investidor (conservador, moderado, arrojado)
        Apresente sugestões práticas e justificadas.
        Use a ferramenta de busca do Google (google_search) para observar as possiveis todas as ameaças dentro do setor financeiro,
        como aumento de taxas, situações que afetam o investimento indiretamente.
        Você também pode usar o (google_search) para encontrar mais
        informações sobre os temas e aprofundar.
        Ao final, você irá escolher as informações mais relevante com base nas suas pesquisas
        e retornar como alerta ao cliente, seus pontos mais relevantes, e um plano abordando as ameaças e como evitalas no futuro.
        """,
        description="Agente que cria plano seguro e cautelo, dentro do perfil do cliente",
        tools=[google_search]
    )

    entrada = f"Carteira atual: {carteira_atual}"

    resultado = call_agent(otimizador, entrada)
    return resultado

# Agente 3: Planejador de Metas e Aportes
def agente_planejador(dados_cliente):
    planejador = Agent(
        name="agente_planejador",
        model="gemini-2.0-flash",
        instruction="""
            Você é um planejador financeiro. Sua tarefa é criar um plano estratégico para o cliente alcançar R$ 1 milhão:
        - Defina metas mensais e anuais
        - Modele aportes crescentes ao longo dos anos
        - Crie cenários conservador, realista e agressivo
        O plano deve ser prático, aplicável e baseado nos dados fornecidos.
        Aponte observações que o cliente deve ser atento.
            """,
        description="Agente planejador de metas financeiras"
    )
    entrada = f"Informações do cliente: {dados_cliente}"

    resultado = call_agent(planejador, entrada)
    return resultado

data_de_hoje = date.today().strftime("%d/%m/%Y")

print("\n📈 Sistema Estratégico para Rumo ao 1 Milhão Ativado! 📈")

print("\nVamos começar com uma análise completa da sua situação atual.")

objetivo = input("\nDigite seu objetivo financeiro ou descrição da sua situação atual:")

if not objetivo:
    print("\n⚠️ Você precisa informar a sua situação financeira para prosseguir!")

else:
    print(f"Beleza! Bora então criar seu plano financeiro {objetivo}")

    print("\n✅ Diagnóstico Inicial")
    resultado1 = agente_diagnostico(objetivo)
    display(to_markdown(resultado1))

    print("\n📊 Otimizando sua carteira")
    resultado2 = agente_otimizador(objetivo)
    display(to_markdown(resultado2))

    print("\n🎯 Criando o Plano Estratégico de Aportes")
    resultado3 = agente_planejador(objetivo)
    display(to_markdown(resultado3))
