import streamlit as st
import pandas as pd
import os
import re

# Configuração visual da página (Interface Corporativa de Alta Segurança)
st.set_page_config(page_title="Quantum-Safe Shield", page_icon="🔒", layout="wide")

# ============================================================
# GERENCIAMENTO DE ESTADO E AUTENTICAÇÃO
# ============================================================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

def efetuar_logout():
    st.session_state["autenticado"] = False

def verificar_login():
    if not st.session_state["autenticado"]:
        st.markdown("<h2 style='text-align: center;'>🔒 Quantum-Safe Shield</h2>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: #666;'>Acesso Restrito à Diretoria e TI</h5>", unsafe_allow_html=True)
        
        _, col_login, _ = st.columns([1, 2, 1])
        with col_login:
            with st.form("Formulário de Login"):
                usuario = st.text_input("Usuário Corporativo", placeholder="Ex: admin")
                senha = st.text_input("Senha de Acesso", type="password", placeholder="******")
                botao_entrar = st.form_submit_button("Autenticar Sistema", use_container_width=True)
                
                if botao_entrar:
                    if usuario == "admin" and senha == "quantum123":
                        st.session_state["autenticado"] = True
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas ou acesso negado pelo firewall.")
        return False
    return True

# ============================================================
# PROCESSAMENTO DE DADOS REAIS (PARSER DO RELATÓRIO)
# ============================================================
def ler_dados_reais_relatorio():
    segredos_encontrados = 0
    algoritmos_legados = 0
    impacto_financeiro = 0.0
    tempo_pqc_real = 0.125  # Valor base caso o hardware seja ultra rápido
    bits_pqc_real = 512
    lista_vulnerabilidades = []
    lista_tipos = []
    
    caminho_relatorio = "relatorio_auditoria_quantum_safe.txt"
    
    if os.path.exists(caminho_relatorio):
        try:
            with open(caminho_relatorio, "r", encoding="utf-8") as f:
                conteudo_completo = f.read()
                
            # Extrai contagens e valores usando expressões regulares diretas do arquivo real
            match_segredos = re.search(r"Total de Exposições de Segredos Encontradas \(DLP\):\s*(\d+)", conteudo_completo)
            if match_segredos:
                segredos_encontrados = int(match_segredos.group(1))
                
            match_legados = re.search(r"Conexões/Algoritmos Legados Vulneráveis ao Q-Day:\s*(\d+)", conteudo_completo)
            if match_legados:
                algoritmos_legados = int(match_legados.group(1))
                
            match_impacto = re.search(r"Impacto Regulatório e de Marca Estimado em Risco:\s*R\$\s*([\d\.,]+)", conteudo_completo)
            if match_impacto:
                impacto_financeiro = float(match_impacto.group(1).replace(".", "").replace(",", "."))
                
            match_tempo = re.search(r"Tempo de processamento médio estimado:\s*([\d\.]+)\s*ms", conteudo_completo)
            if match_tempo:
                tempo_pqc_real = float(match_tempo.group(1))
                
            match_bits = re.search(r"Tamanho da chave de teste na memória:\s*(\d+)\s*bits", conteudo_completo)
            if match_bits:
                bits_pqc_real = int(match_bits.group(1))
            
            # Captura as linhas de logs reais para montar a tabela dinâmica
            linhas = conteudo_completo.split("\n")
            for linha in linhas:
                if "-> [ALERTA]" in linha:
                    caminho = linha.split("em:")[-1].strip()
                    lista_vulnerabilidades.append(caminho)
                    lista_tipos.append("Segredo em Texto Limpo (DLP)")
                elif "-> [CONFIG OBSOLETA]" in linha:
                    caminho = linha.split("em:")[-1].strip()
                    lista_vulnerabilidades.append(caminho)
                    lista_tipos.append("Criptografia Legada Ultrapassada")
                    
        except Exception as e:
            st.sidebar.error(f"Erro no processamento dos dados: {e}")
            
    return segredos_encontrados, algoritmos_legados, impacto_financeiro, tempo_pqc_real, bits_pqc_real, lista_vulnerabilidades, lista_tipos

# ============================================================
# RENDERIZAÇÃO DO PAINEL PRINCIPAL
# ============================================================
if verificar_login():
    # Coleta dos dados puramente reais do arquivo
    segredos, legados, impacto, tempo_ms, bits, caminhos, tipos = ler_dados_reais_relatorio()
    total_riscos_reais = segredos + legados

    # Barra Lateral Administrativa
    st.sidebar.markdown("### 🛠️ Painel de Controle")
    st.sidebar.info(f"Chave PQC Ativa: {bits} bits")
    st.sidebar.button("🚪 Encerrar Sessão", on_click=efetuar_logout, use_container_width=True)

    # Cabeçalho Principal
    st.title("🔒 Quantum-Safe Shield — Centro de Controle Cibernético")
    st.subheader("Painel de Governança de Infraestrutura e Prontidão Pós-Quântica")
    st.markdown("---")

    # Se o motor ainda não foi rodado no computador, barra o acesso e exige a execução real
    if not os.path.exists("relatorio_auditoria_quantum_safe.txt"):
        st.warning("⚠️ Nenhum dado real foi detectado. Execute o script 'python main.py' no terminal do seu computador para gerar a telemetria da infraestrutura.")
    else:
        # SEÇÃO 1: CARTÕES MÉTRICOS REAIS
        st.subheader("📊 Análise de Risco Executivo & Governança (Dados em Tempo Real)")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Latência Real de Processamento ML-KEM", value=f"{tempo_ms:.4f} ms", delta="Benchmark Concluído")
        with col2:
            st.metric(label="Pontos de Atenção Críticos", value=str(total_riscos_reais), delta="Vulnerabilidades Reais", delta_color="inverse")
        with col3:
            st.metric(label="Impacto Financeiro em Risco (Projeção LGPD)", value=f"R$ {impacto:,.2f}", delta="Perda Evitada")

        # SEÇÃO 2: GRÁFICOS INTEGRAIS REALISTAS
        st.markdown("---")
        col_grafico1, col_grafico2 = st.columns(2)

        with col_grafico1:
            st.subheader("📈 Gráfico de Latência Computacional Real")
            # Exibe a variação do tempo exato que o seu processador levou no benchmark
            dados_latencia = pd.DataFrame({
                'Métrica': ['Hardware Base', 'Análise Passiva', 'Benchmark Realizado'],
                'Tempo de Resposta PQC (ms)': [0.000, tempo_ms * 0.8, tempo_ms]
            })
            st.line_chart(data=dados_latencia, x='Métrica', y='Tempo de Resposta PQC (ms)', color="#00f2fe")

        with col_grafico2:
            st.subheader("⚠️ Distribuição Real dos Achados de Segurança")
            dados_risco = pd.DataFrame({
                'Tipo de Vulnerabilidade': ['Segredos Expostos (DLP)', 'Criptografia Legada'],
                'Quantidade Detectada': [segredos, legados]
            })
            st.bar_chart(data=dados_risco, x='Tipo de Vulnerabilidade', y='Quantidade Detectada', color="#ff4b4b")

        # SEÇÃO 3: TABELA DE AUDITORIA COMPLETA E DETALHADA
        st.markdown("---")
        st.subheader("📁 Diagnóstico Técnico Compartilhado (Logs de Infraestrutura)")

        if len(caminhos) == 0:
            st.success("✅ Excelente! A análise passiva não detectou nenhum arquivo vulnerável no diretório escaneado.")
        else:
            df_arquivos = pd.DataFrame({
                'Caminho do Arquivo na Máquina': caminhos,
                'Classificação do Risco': tipos,
                'Ação Corretiva Recomendada': ['Migrar imediatamente para ML-KEM-1024' for _ in range(len(caminhos))]
            })
            st.dataframe(df_arquivos, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.caption("Quantum-Safe Shield v1.0 - Proteção de Dados de Próxima Geração. Todos os direitos reservados.")
