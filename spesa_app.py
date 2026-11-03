import pandas as pd
import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Spesa Smart - Terzo Settore", page_icon="🛒", layout="wide"
)

st.title("🛒 Spesa Smart & Monitoraggio Prezzi (€/kg)")
st.markdown(
    "*Strumento operativo di trasparenza per il Terzo Settore: confronto prezzi medi e calcolo spesa totale minima tra i 5 Supermercati (A, B, C, D, E) e Bancherella Mercato.*"
)

# Elenco univoco e rigido dei 6 canali a confronto
CANALI_COMMERCIALI = [
    "Supermercato A",
    "Supermercato B",
    "Supermercato C",
    "Supermercato D",
    "Supermercato E",
    "Bancherella Mercato",
]

# Tabella di riferimento con prezzi medi di prova (aggiornabili)
dati_prezzi_medi = {
    "Categoria ISTAT Neutra": [
        "Pane Comune (€/kg)",
        "Ortaggi Freschi (€/kg)",
        "Olio Extravergine (€/L)",
        "Passata di Pomodoro (€/kg)",
        "Pasta di Semola (€/kg)",
    ],
    "Supermercato A": [2.90, 2.20, 9.50, 1.80, 1.45],
    "Supermercato B": [2.80, 2.50, 8.90, 1.60, 1.35],
    "Supermercato C": [2.10, 1.90, 7.50, 1.20, 1.10],
    "Supermercato D": [2.60, 2.10, 8.80, 1.50, 1.30],
    "Supermercato E": [2.70, 2.30, 8.70, 1.55, 1.32],
    "Bancherella Mercato": [2.00, 1.40, 7.80, 1.30, 1.20],
}

df_prezzi_medi = pd.DataFrame(dati_prezzi_medi)

# Creazione dei 5 Tab dell'applicazione
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Inserimento Prezzi",
        "⚖️ Calcolo Prezzo/Kg",
        "🤝 Tabella Prezzi Medi",
        "🔍 Analisi & Asimmetrie",
        "🎯 Tab 5: Calcolo Spesa Totale Minore",
    ]
)

# --- TAB 1: Inserimento Rilevazione ---
with tab1:
    st.header("1. Inserimento Rilevazione Prodotto")
    col1, col2 = st.columns(2)

    with col1:
        prodotto_nome = st.text_input(
            "Denominazione / Prodotto",
            placeholder="Es. Passata di pomodoro / Pane comune",
        )
        canale_vendita = st.selectbox(
            "Seleziona Esercente / Canale", CANALI_COMMERCIALI
        )

    with col2:
        prezzo_conf = st.number_input(
            "Prezzo Confezione (€)", min_value=0.0, format="%.2f"
        )
        peso_valore = st.number_input(
            "Quantità / Peso Dichiarato", min_value=0.0, format="%.2f"
        )
        unita_peso = st.selectbox("Unità di Misura", ["kg", "hg", "g", "L"])

    categoria_istat = st.selectbox(
        "Associa a Categoria Neutra ISTAT",
        df_prezzi_medi["Categoria ISTAT Neutra"].tolist(),
    )

# --- TAB 2: Normalizzazione Prezzo ---
with tab2:
    st.header("2. Normalizzazione Matematica (€/kg o €/L)")


    def calcola_prezzo_standard(prezzo, valore, unita):
        if unita == "hg":
            q_kg = valore / 10.0
        elif unita == "g":
            q_kg = valore / 1000.0
        else:
            q_kg = valore
        if q_kg > 0:
            return round(prezzo / q_kg, 2)
        return 0.0


    prezzo_unitario = calcola_prezzo_standard(
        prezzo_conf, peso_valore, unita_peso
    )
    st.metric(
        label="Prezzo Normalizzato Calcolato",
        value=f"{prezzo_unitario} €/kg (o €/L)",
    )

# --- TAB 3: Tabella Prezzi Medi ---
with tab3:
    st.header(
        "🤝 Confronto Prezzi Medi: Supermercati A, B, C, D, E vs Bancherella Mercato"
    )
    st.markdown(
        "I prezzi medi indicati in tabella si riferiscono **esclusivamente** ai 5 supermercati censiti e alla bancherella."
    )
    st.dataframe(df_prezzi_medi, use_container_width=True)

# --- TAB 4: Analisi & Asimmetrie ---
with tab4:
    st.header("🔍 Analisi delle Asimmetrie Informative e Trasparenza")
    st.markdown(
        "Modulo di verifica per contrastare le denominazioni ingannevoli e l'assenza del retro-etichetta nel commercio digitale."
    )
    st.info(
        "La normalizzazione a parità di unità di misura consente di ristabilire il corretto consenso informato all'acquisto."
    )

# --- TAB 5: Calcolo Spesa Totale Minore ---
with tab5:
    st.header(
        "🎯 Tab 5: Seleziona la Lista della Spesa e Trova il Canale più Economico"
    )
    st.markdown(
        "Seleziona i prodotti necessari alla famiglia e indica la quantità desiderata."
    )

    # Box di istruzioni pratiche chiarissime per l'inserimento
    st.info(
        "💡 **Istruzioni per l'inserimento delle quantità (in kg o litri):**\n"
        "- I valori si inseriscono in **decimali**. Ad esempio:\n"
        "  * **0.50 kg** = mezzo chilo (**500 g / 5 hg**)\n"
        "  * **0.25 kg** = un quarto di chilo (**250 g / 2,5 hg**)\n"
        "  * **1.00 kg** = un intero chilo o litro\n"
        "- Usa i pulsanti **+** e **-** per regolare la quantità a scatti di 1 ettogrammo (`0.10 kg`)."
    )

    prodotti_scelti = st.multiselect(
        "Seleziona i prodotti da inserire nella lista della spesa:",
        df_prezzi_medi["Categoria ISTAT Neutra"].tolist(),
        default=[
            "Pane Comune (€/kg)",
            "Pasta di Semola (€/kg)",
            "Passata di Pomodoro (€/kg)",
        ],
    )

    if prodotti_scelti:
        st.subheader("Quantità richieste per ciascun prodotto:")
        quantita_dict = {}
        col_q1, col_q2 = st.columns(2)

        for i, prod in enumerate(prodotti_scelti):
            with col_q1 if i % 2 == 0 else col_q2:
                quantita_dict[prod] = st.number_input(
                    f"Quantità (kg/L) per: {prod}",
                    min_value=0.05,
                    value=0.50,
                    step=0.10,
                    format="%.2f",
                    key=f"q_{prod}",
                )

        if st.button("Calcola Spesa Totale per Canale"):
            totali_canali = {}
            for canale in CANALI_COMMERCIALI:
                totale_canale = 0.0
                for prod in prodotti_scelti:
                    prezzo_unit = df_prezzi_medi.loc[
                        df_prezzi_medi["Categoria ISTAT Neutra"] == prod, canale
                    ].values[0]
                    totale_canale += prezzo_unit * quantita_dict[prod]
                totali_canali[canale] = round(totale_canale, 2)

            df_totali = pd.DataFrame(
                list(totali_canali.items()),
                columns=["Canale di Vendita", "Spesa Totale Stimata (€)"],
            )
            df_totali = df_totali.sort_values(
                by="Spesa Totale Stimata (€)"
            ).reset_index(drop=True)

            st.success("📊 **Risultato del Confronto Spesa Totale:**")
            st.dataframe(df_totali, use_container_width=True)

            miglior_canale = df_totali.iloc[0]["Canale di Vendita"]
            miglior_prezzo = df_totali.iloc[0]["Spesa Totale Stimata (€)"]

            st.markdown(
                f"### 🏆 Il canale con il **prezzo totale inferiore** per questa lista è: **{miglior_canale}** con un totale di **€ {miglior_prezzo:.2f}**."
            )
    else:
        st.warning(
            "Seleziona almeno un prodotto dalla lista per avviare il calcolo."
        )