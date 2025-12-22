"""
Holds the translations of paper keywords on supported langagues. 
"""

from enum import Enum

class Keywords_PT_BR(Enum):
    LANG_CODE = "PT_BR"
    REFERENCES = "REFERÊNCIAS"
    ABSTRACT = "RESUMO"
    KEYWORDS = "PALAVRAS-CHAVE"
    ARTIFACTS = "DISPONIBILIDADE DE ARTEFATO"
    ACKS = "AGRADECIMENTOS"

class Keywords_EN(Enum):
    LANG_CODE = "EN"
    REFERENCES = "REFERENCES"
    ABSTRACT = "ABSTRACT"
    KEYWORDS = "KEYWORDS"
    ARTIFACTS = "ARTIFACT AVAILABILITY"
    ACKS = "ACKNOWLEDGMENTS"

LANGUAGES = [Keywords_EN, Keywords_PT_BR]  
