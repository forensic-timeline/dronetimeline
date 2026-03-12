"""
Entity Recognition Module

Uses spaCy's EntityRuler with custom JSONL rules to detect and annotate
forensic entities in timeline text (IP addresses, HTTP codes, registry keys, etc.).
"""

import os
import spacy
from spacy.lang.en import English


class EntityRecognition:
    """
    Rule-based entity recognition for forensic timeline analysis.
    
    Uses spaCy's EntityRuler with two sets of rules:
    - rules.jsonl: Base patterns (IPs, URLs, ports, registry keys, etc.)
    - entity_dependend_rules.jsonl: Patterns that depend on already-found entities
    
    Attributes:
        nlp: spaCy Language pipeline with entity rulers loaded
    """

    def __init__(self, rules_dir: str = None):
        """
        Initialize the EntityRecognition engine.
        
        Args:
            rules_dir: Path to directory containing JSONL rule files.
                       Defaults to the 'rules' subdirectory of this module.
        """
        self.nlp = English()

        if rules_dir is None:
            rules_dir = os.path.join(os.path.dirname(__file__), "rules")

        rules_path = os.path.join(rules_dir, "rules.jsonl")
        entity_dep_rules_path = os.path.join(rules_dir, "entity_dependend_rules.jsonl")

        self.nlp.add_pipe(
            "entity_ruler",
            config={"overwrite_ents": "true"}
        ).from_disk(rules_path)

        self.nlp.add_pipe(
            "entity_ruler",
            name="entity_dependend_ruler",
            config={"overwrite_ents": "true"}
        ).from_disk(entity_dep_rules_path)

    def find_entity(self, text: str) -> tuple:
        """
        Find entities in a text string and return annotated HTML.
        
        Detected entities are wrapped in HTML bold tags with yellow background
        and labeled subscripts.
        
        Args:
            text: The input text to analyze
        
        Returns:
            Tuple of (annotated_html_string, spacy_doc, list_of_entities)
        """
        doc = self.nlp(text)
        list_of_matches = []
        entities = []

        for ent in doc.ents:
            matched_string = ent.text
            string_id = ent.ent_id_

            matched_details = self._string_slicer(doc, ent.start, ent.end, matched_string, string_id)
            list_of_matches.append(matched_details)
            entities.append(ent)

        # Apply markings from end to start to preserve character indices
        result = text
        for matched_details in reversed(list_of_matches):
            marked_string = matched_details[0]
            start_char_index = matched_details[1]
            end_char_index = matched_details[2]

            result = (
                result[:start_char_index]
                + marked_string
                + result[end_char_index:]
            )

        return result, doc, entities

    def _string_slicer(self, doc, start: int, end: int, matched_string: str, string_id: str) -> tuple:
        """
        Create HTML-annotated replacement string for a matched entity.
        
        Args:
            doc: spaCy Doc object
            start: Token start index
            end: Token end index
            matched_string: The matched text
            string_id: The entity rule ID
        
        Returns:
            Tuple of (html_string, start_char_index, end_char_index)
        """
        start_char_index = doc[start:end].start_char
        end_char_index = doc[start:end].end_char

        marked = f'<b style="background-color:yellow;"> {matched_string} </b>'
        return marked, start_char_index, end_char_index

    def iob_format(self, doc, entities: list) -> list:
        """
        Convert entity annotations to IOB (Inside-Outside-Beginning) format.
        
        Args:
            doc: spaCy Doc object
            entities: List of spaCy Entity spans
        
        Returns:
            List of (tag, token) tuples in IOB format
        """
        array = [('O', token) for token in doc]

        for ent in entities:
            label = ent.label_
            array[ent.start] = (f'B-{label}', doc[ent.start])
            for i in range(ent.start + 1, ent.end):
                array[i] = (f'I-{label}', doc[i])

        return array
