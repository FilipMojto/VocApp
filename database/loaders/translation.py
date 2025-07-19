
# SEEDER_FILE_PATH = './seeds/words.json'

# import json
# import sqlite3

# import os, sys
# from typing import List

# # Ensure the path to the seeds directory is in the system path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')


# from shared.vocapptypes import Translation

# def load_words_json() -> List[Translation]:
#     with open(SEEDER_FILE_PATH, 'r', encoding='utf-8') as file:
#         lexical_entries = json.load(file)

#     translations: List[Translation] = []

#     for entry in lexical_entries:
#         translations = entry.get('translations', [])
#         for translation in translations:
#             translation_obj = Translation(
#                 lexeme=translation['text'],
#                 category=translation.get('category', 'neutral'),
#                 wordpack=translation.get('wordpack', 'basic')
#             )
#             translations.append(translation_obj)

#     return translations
    

#     # for entry in lexical_entries:
        
#     #     for translation in entry.get('translations', []):
#     #         cursor.execute(
#     #             "INSERT INTO translations (lexeme, category, wordpack) VALUES (?, ?, ?)",
#     #             (entry['word'], translation['category'], translation['wordpack'])
#     #         )
    
        
#     # return lexical_entries



