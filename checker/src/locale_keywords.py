"""
Holds the translations of paper keywords on supported langagues. 
"""

from enum import Enum

class Keywords_PT_BR(Enum):
    LANG_CODE = "PT_BR"
    REFERENCES = "REFERÊNCIAS"
    ABSTRACT = "Resumo"
    KEYWORDS = "Palavras-chave"
    ARTIFACTS = "Disponibilidade de Artefatos"
    WRONG_ARTIFACTS = ("DISPONIBILIDADE DE ARTEFATO","DISPONIBILIDADE DE ARTEFATO", "Disponibilidade de Artefato")
    ACKS = "Agradecimentos"
    WRONG_ACKS = ("AGRADECIMENTO", "AGRADECIMENTOS", "Agradecimento")
    BIOGRAPHY_REGEX = r'[Bb]iografia'

class Keywords_EN(Enum):
    LANG_CODE = "EN"
    REFERENCES = "REFERENCES"
    ABSTRACT = "Abstract"
    KEYWORDS = "Keywords"
    ARTIFACTS = "Artifact Availability"
    WRONG_ARTIFACTS = ("ARTIFACTS AVAILABILITY", "ARTIFACT AVAILABILITY")
    ACKS = "Acknowledgments"
    WRONG_ACKS = ("ACKNOWLEDGMENT", "ACKNOWLEDGMENTS", "Acknowledgement")
    BIOGRAPHY_REGEX = r'[Bb]iograph'

LANGUAGES = [Keywords_EN, Keywords_PT_BR]  
