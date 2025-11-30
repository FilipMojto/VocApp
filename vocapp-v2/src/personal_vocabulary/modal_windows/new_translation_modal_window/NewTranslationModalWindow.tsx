import type { WordCreate } from "../../../api/types";
import { relationTypes, type RelationType } from "../../crud/WordRelation";
import {
  type ModalWindowBaseProps,
  VocapModalWindow,
  type MLInput,
  type MLSelect,
  type VocapModalWindowForm,
} from "../base";
import "./NewTranslationModelWindow.css";
import { useState } from "react";

export interface TranslationModalWindowForm extends VocapModalWindowForm {
  translation: WordCreate;
  relationType: RelationType;
};

export interface NewTranslationModalWindowProps extends ModalWindowBaseProps {
  initialText?: string;
  initialRelationType?: RelationType;
  initialCategory?: string;
  initialPack?: string;
  initialLangCode?: string;
  // onAdd?: (payload: VocapModalWindowForm) => void;
};

function NewTranslationModalWindow({
  initialText = "",
  initialRelationType = "translation",
  initialCategory = "neutral",
  initialPack = "basic",
  initialLangCode = "en",
  onCancel,
  onAdd,
}: NewTranslationModalWindowProps) {
  const [text, setText] = useState(initialText);
  const [relationType, setRelationType] = useState(initialRelationType);
  const [category, setCategory] = useState(initialCategory);
  const [pack, setPack] = useState(initialPack);
  const [langCode, setLangCode] = useState(initialLangCode);
    const options = relationTypes.map((value) => ({
    value,
    label: value.charAt(0).toUpperCase() + value.slice(1),
    group: value === "translation" ? "Basic" : "Advanced",
    }));
  const submit = async () => {
    if (!text.trim()) {
      return Promise.reject(new Error("Please enter the translation text."));
    }

    // setSubmitting(true);
    const payload: TranslationModalWindowForm = {
    //   : text.trim(),
      translation: {
        lexeme: text.trim(),
        category: (category ?? initialCategory).toString().toLowerCase(),
        wordpack: (pack ?? initialPack).toString().toLowerCase(),
        language_code: (langCode ?? initialLangCode).toString().toLowerCase(),
      },
      relationType: relationType ?? initialRelationType,
    };

    // If caller provided onAdd, call it (could POST to backend there).
    if (onAdd) {
      await Promise.resolve(onAdd(payload));
    } else {
      // fallback behavior: just log
      console.log("Add translation (no onAdd provided):", payload);
    }
    // optionally reset fields:
    setText("");
    setRelationType(initialRelationType);
    setCategory(initialCategory);
    setPack(initialPack);
    setLangCode(initialLangCode);

    return Promise.resolve();
  };

  return (
    <VocapModalWindow
      headerTitle="New Translation"
      onSubmit={submit}
      onCancel={onCancel}
      rows={[
        {
          fields: [
            {
              label: "Lexeme",
              placeholder: "Enter new lexeme…",
              defaultValue: text,
              onChange: (e) => setText(e.target.value),
            } as MLInput,
            {
              id: "ntmw-pack",
              label: "Relation Type",
              defaultValue: pack,
              onChange: (e) => setPack(e.target.value),
              options: options,
            } as MLSelect,
          ],
        },
        {
          fields: [
            {
              id: "ntmw-category",
              label: "Category",
              defaultValue: category,
              onChange: (e) => setCategory(e.target.value),
              options: [
                { value: "neutral", label: "Neutral" },
                { value: "formal", label: "Formal" },
                { value: "informal", label: "Informal" },
                { value: "idiomatic", label: "Idiomatic" },
              ],
            } as MLSelect,
            {
              id: "ntmw-pack",
              label: "Pack",
              defaultValue: pack,
              onChange: (e) => setPack(e.target.value),
              options: [
                { value: "basic", label: "Basic" },
                { value: "furniture", label: "Furniture" },
              ],
            } as MLSelect,
            {
              id: "ntmw-lang-code",
              label: "Lang Code",
              defaultValue: langCode,
              onChange: (e) => setLangCode(e.target.value),
              options: [
                { value: "en", label: "English" },
                { value: "sk", label: "Slovak" },
                { value: "de", label: "German" },
              ],
            } as MLSelect,
          ],
        },
      ]}
    />
  );
}

export default NewTranslationModalWindow;
