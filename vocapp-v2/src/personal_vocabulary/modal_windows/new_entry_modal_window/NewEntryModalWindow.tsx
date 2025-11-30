import "../new_translation_modal_window/NewTranslationModelWindow.css";

import { useState } from "react";
import type { WordCreate } from "../../../api/types";
import {
  type ModalWindowBaseProps,
  VocapModalWindow,
  type MLInput,
} from "../base";

export const INITIAL_LEXEME = "";
export const INITIAL_LANG_CODE = "en";
export const INITIAL_CATEGORY = "neutral";
export const INITIAL_WORDPACK = "basic";

interface NewEntryModalWindowState extends ModalWindowBaseProps {
  initialLexeme?: string;
  initialLanguageCode?: string;
  initialCategory?: string;
  initialWordpack?: string;
  onAdd: (payload: WordCreate) => void | Promise<void>;
}

export function NewWordModalWindow({
  initialLexeme = INITIAL_LEXEME,
  initialLanguageCode = INITIAL_LANG_CODE,
  initialCategory = INITIAL_CATEGORY,
  initialWordpack = INITIAL_WORDPACK,
  onAdd,
  onCancel,
}: NewEntryModalWindowState) {
  const [lexeme, setLexeme] = useState(initialLexeme);
  const [language_code, setLanguageCode] = useState(initialLanguageCode);
  const [category, setCategory] = useState(initialCategory);
  const [wordpack, setWordpack] = useState(initialWordpack);

  const submit = async () => {
    if (!lexeme.trim()) {
      return Promise.reject(new Error("Please enter the lexeme."));
    }

    const payload: WordCreate = {
      lexeme: lexeme.trim(),
      language_code: language_code.trim().toLocaleLowerCase(),
      wordpack: wordpack.trim(),
      category: category.trim(),
    };

    console.log("payload", payload);

    if (onAdd) {
      await Promise.resolve(onAdd(payload));
    } else {
      console.log("No onAdd handler provided.");
    }

    setLexeme("");
    return Promise.resolve();
  };

  return (
    <VocapModalWindow
      headerTitle="Add New Lexical Entry"
      onSubmit={submit}
      onCancel={onCancel}
      rows={[
        {
          fields: [
            {
              label: "Lexeme",
              placeholder: "Enter new lexeme…",
              defaultValue: lexeme,
              onChange: (e) => setLexeme(e.target.value),
            } as MLInput,
            {
              label: "Category",
              options: [
                { value: "neutral", label: "Neutral" },
                { label: "formal", value: "Formal" },
                { label: "informal", value: "Informal" },
                { label: "idiomatic", value: "Idiomatic" },
              ],
              onChange: (e) => setCategory(e.target.value),
              defaultValue: category,
            } as MLInput,
            {
              label: "Wordpack",
              options: [
                { value: "basic", label: "Basic" },
                { value: "furniture", label: "Furniture" },
              ],
              onChange: (e) => setWordpack(e.target.value),
              defaultValue: wordpack,
            } as MLInput,
            {
              label: "Language",
              options: [
                { value: "en", label: "English" },
                { value: "sk", label: "Slovak" },
              ],
              defaultValue: language_code,
              onChange: (e) => setLanguageCode(e.target.value),
            } as MLInput,
          ],
        },
      ]}
    ></VocapModalWindow>
  );
}
