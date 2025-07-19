# __ALL__ = ['load_lexical_entries_json']

# import sqlite3
# import json
# from typing import List
# import os, sys

# # Ensure the path to the seeds directory is in the system path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

# from shared.vocapptypes import LexicalEntry, Translation

# def load_lexical_entries_json() -> List[LexicalEntry]:
#     SEEDER_FILE_PATH = './seeds/lexical_entries.json'
    
#     with open(SEEDER_FILE_PATH, 'r', encoding='utf-8') as file:
#         lexical_entries_data = json.load(file)

#     lexical_entries: List[LexicalEntry] = []

#     for entry in lexical_entries_data.get('entries', []):
#         translations = entry.get('translations', [])
#         translation_objects = [
#             Translation(
#                 lexeme=translation['text'],
#                 category=translation.get('category', 'neutral'),
#                 wordpack=translation.get('wordpack', 'basic')
#             ) for translation in translations
#         ]

#          # Create a LexicalEntry object with the word and its translations

#         lexical_entry = LexicalEntry(
#             word=entry['word'],
#             translations=translation_objects
#         )

#         lexical_entries.append(lexical_entry)

#     return lexical_entries
