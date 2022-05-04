import re
from collections import Counter

import streamlit as st


def identificar(est: str, processo: str) -> None:
    estereotipos_encontrados = re.findall(est, processo, re.IGNORECASE)
    resultado = Counter(estereotipos_encontrados)

    for estereotipo, contagem in resultado.items():
        st.text(f"Estereótipo: {estereotipo} aparece {contagem} vez(es)")
