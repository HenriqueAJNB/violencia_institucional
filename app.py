import pathlib
import re
import string
from collections import Counter

import nltk
import streamlit as st
from nltk.tokenize import wordpunct_tokenize
from tika import parser

from padroes import identificar

nltk.download("punkt")
nltk.download("stopwords")

st.markdown("# COMBATE À VIOLÊNCIA INSTITUCIONAL CONTRA A MULHER ")
pdfs = st.file_uploader(
    label="Faça o upload dos pdfs (200M por arquivo) dos processos a serem analisados",
    type="pdf",
    accept_multiple_files=True,
)

pasta_raiz = pathlib.Path().absolute()

for pdf in pdfs:
    if pdf != None:
        processo_txt = pdf.name.replace("pdf", "txt")
        arquivo_processo_txt = pasta_raiz / processo_txt
        if not arquivo_processo_txt.exists():
            parsed = parser.from_file(str(pasta_raiz / pdf.name))
            with open(arquivo_processo_txt, "w", encoding="utf_8") as f:
                f.write(parsed["content"])

        with open(arquivo_processo_txt, "r", encoding="utf_8") as f:
            processo = f.read()

        # Transformando processo para minúsculo
        processo = processo.lower()

        # Removendo as pontuações
        for pontuacao in string.punctuation:
            processo = processo.replace(pontuacao, "")

        tokens_processo = wordpunct_tokenize(processo)

        # eliminar stopwords (palavras que podem ser removidas e a frase continuar com sentido)
        list_stopwords = nltk.corpus.stopwords.words("portuguese")

        for sw in list_stopwords:
            tokens_processo = list(filter(lambda token: token not in sw, tokens_processo))

        # REGEX 01 (vingativa-o)
        lista_estereotipos = [
            "vingativ[o|a]",
            "louc[o|a]",
            "descontrolad[o|a]",
            "descontrole emocional",
            "instabilidade emocional",
            "temperamento difícil",
        ]

        for estereotipo in lista_estereotipos:
            identificar(estereotipo, processo)

    st.markdown(f"##### Número do processo: {pdf.name.replace('.pdf', '')}")
    # st.text(
    #     f"Foi(foram) encontrado(s) no total {len(resultado_est_1)} estereótipo(s) de gênero neste processo."
    # )

if pdfs:
    st.markdown(
        "**Uma vez identificado(s) o(s) estereótipo(s) de gênero, analise o contexto para confirmar a ocorrência ou não de violência institucional.**"
    )
