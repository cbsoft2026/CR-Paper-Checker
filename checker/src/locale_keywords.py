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
    WRONG_ARTIFACTS = ("DISPONIBILIDADE DE ARTEFATOS", "Disponibilidade de Artefato")
    ACKS = "AGRADECIMENTOS"
    WRONG_ACKS = ("AGRADECIMENTO", "Agradecimentos", "Agradecimento")

class Keywords_EN(Enum):
    LANG_CODE = "EN"
    REFERENCES = "REFERENCES"
    ABSTRACT = "ABSTRACT"
    KEYWORDS = "KEYWORDS"
    ARTIFACTS = "ARTIFACT AVAILABILITY"
    WRONG_ARTIFACTS = ("ARTIFACTS AVAILABILITY", "Artifact Availability")
    ACKS = "ACKNOWLEDGMENTS"
    WRONG_ACKS = ("ACKNOWLEDGMENT", "Acknowledgments", "Acknowledgment")

LANGUAGES = [Keywords_EN, Keywords_PT_BR]  
