import { useCallback, useEffect, useRef, useState } from "react";
import ButtonIconContainer from "../components/icon_slots/label_icon_container/ButtonIconContainer";

import type { ModalWindowMode } from "./PersonalVocabulary";
import { type RelationType, type WordRelation } from "./crud/WordRelation";
import NewTranslationModalWindow, {
  type TranslationModalWindowForm,
} from "./modal_windows/new_translation_modal_window/NewTranslationModalWindow";
import api, { WORD_RELATION_PREFIX } from "../api/api";
import { useAuth } from "../user_account/auth_context/AuthContext";
import type { RelationEntry, Word, WordCreate } from "../api/types";
import { edit_entry } from "./crud";

export const DEF_RELATION_TYPE: RelationType = "translation";

// add these states near your other states
export type TranslationsStatus =
  | "idle"
  | "loading"
  | "no-mappings"
  | "error"
  | "loaded";

export interface TranslationPanelProps {
  entries: Word[];
  // selectedEntryId: number | null;
  selectedWord: Word | undefined;
}

function TranslationPanel({
  entries,
  // selectedEntryId,
  selectedWord,
}: TranslationPanelProps) {
  const { user } = useAuth(); // call hook here, at top level of component
  const [translations, setTranslations] = useState<RelationEntry[]>([]);
  const [selectedTranslation, setSelectedTranslation] = useState<
    RelationEntry | undefined
  >(undefined);
  const [translationsStatus, setTranslationsStatus] =
    useState<TranslationsStatus>("idle");
  const [translationsError, setTranslationsError] = useState<string | null>(
    null
  );
  const [newTranslationModalWindowMode, setNewTranslationModalWindowMode] =
    useState<ModalWindowMode>("hidden");
  // const [translation, setTranslation] = useState<Word | null>(null);
  const latestTranslationsReqId = useRef(0);

  const isEntrySelected = (alert_user: boolean = false) => {
    if (!selectedWord || !selectedWord.id) return false;

    if (alert_user && selectedWord.id === null) {
      alert("Please select a lexical entry first.");
      return false;
    }

    return true;
  };

  const refreshTranslations = () => {
    if (selectedWord && selectedWord.id) {
      console.log("Refreshing translations...");
      fetchTranslations(selectedWord.id); // refresh directly
      return true;
    } else {
      console.log("Refreshing failed: Entry not selected.");
      return false;
    }
  };

  const onAddTranslation = () => {
    if (!isEntrySelected(true)) {
      alert("Please select a lexical entry first.");
      return;
    }

    // setTranslation(null); // ensure no pre-filled data
    setNewTranslationModalWindowMode("adding");
    console.log("Add Translation clicked");
  };

  const onEditTranslation = () => {
    if (!isEntrySelected(true)) {
      alert("Please select a lexical entry first.");
      return;
    }

    setNewTranslationModalWindowMode("editing");
    console.log("Edit Translation clicked");
  };

  const onDeleteTranslation = async () => {
    console.log("Delete Translation clicked");
    if (selectedTranslation) {
      await deleteTranslation(selectedTranslation);

      setTranslations((prev) => prev.filter((t) => t.id !== selectedTranslation.id));
      setSelectedTranslation(undefined);
    } else {
      alert("Please select a translation to delete.");
    }
  };

  // fetcher used by the effect and manually after adding a new translation
  const fetchTranslations = useCallback(
    async (id: number | null) => {
      console.log("Fetchibn")
      if (!user || id == null) return;

      if (id == null) {
        setTranslations([]);
        setTranslationsStatus("idle");
        return;
      }

      const reqId = ++latestTranslationsReqId.current;
      setTranslationsStatus("loading");
      setTranslationsError(null);

      try {
        const res = await api.get<RelationEntry[]>(
          `${WORD_RELATION_PREFIX}/${id}`,
          {
            params: {
              relation_type: DEF_RELATION_TYPE,
            },
          }
        );
        console.log("Fetched", res.data)

        if (reqId !== latestTranslationsReqId.current) return; // stale

        setTranslations(res.data ?? []);
        console.log("Updated translations", translations)
        setTranslationsStatus("loaded");
      } catch (err: any) {
        if (reqId !== latestTranslationsReqId.current) return; // stale
        const status = err?.response?.status;
        if (status === 404) {
          setTranslations([]);
          setTranslationsStatus("no-mappings");
        } else {
          setTranslations([]);
          setTranslationsStatus("error");
          setTranslationsError(err?.message ?? "Failed to load translations");
        }
      }
    },
    [user]
  );

  // run on entryId change — fetchTranslations is stable via useCallback
  useEffect(() => {
    if (selectedWord) {
      fetchTranslations(selectedWord.id);
    } else {
      fetchTranslations(null);
    }
    // dependencies: entryId and fetchTranslations (which depends on get_translations)
  }, [selectedWord, fetchTranslations]);

  // Example onAdd: add translation, link it, then refresh translations by calling fetchTranslations(entryId)
  const createTranslation = useCallback(
    async (translationForm: TranslationModalWindowForm) => {
      console.log("New translation to add:", translationForm);

      if (!selectedWord || !isEntrySelected(true)) {
        return;
      }

      await api
        .post<WordRelation>(WORD_RELATION_PREFIX, translationForm.translation, {
          params: {
            word_id: selectedWord.id,
            relation_type: translationForm.relationType,
          },
        })
        .then((res) => {
          console.log("Translation added:", res.data);

          setNewTranslationModalWindowMode("hidden");
          // setTranslation(null);
          // console.log("Selected", selectedWord);
          refreshTranslations();

          // if (selectedWord.id) {
          //   console.log("fetching...");
          //   fetchTranslations(selectedWord.id); // refresh directly
          // }
        });
    },
    [selectedWord, fetchTranslations]
  );

  const editTranslation = async (
    translatioForm: TranslationModalWindowForm
  ) => {
    console.log("New translation to edit:", translatioForm.translation);

    if (!selectedWord || !isEntrySelected(true) || !selectedTranslation) {
      return;
    }

    await edit_entry(translatioForm.translation, selectedTranslation.id).then(
      (res) => {
        console.log("Translation edited:", res.data);
        setNewTranslationModalWindowMode("hidden");
        refreshTranslations();
      }
    );
  };

  const deleteTranslation = async (entry: RelationEntry) => {
    console.log("New relation entry to delete: ", entry);

    const res = await api.delete<WordRelation>(WORD_RELATION_PREFIX, {
      data: entry,
    });

    return res;
  };

  function onTranslationRowClick(
    event: React.MouseEvent<HTMLTableRowElement>,
    id: number
  ): void {
    const translation = translations.find((t) => t.id === id);
    setSelectedTranslation(translation);
  }

  return (
    <section
      id="pvw-mapped-translations-section"
      className="pvw-card table-card"
    >
      <h2 className="section-title">
        {/* {`'${selectedWord?.lexeme ?? ""}' - Mapped translations`} */}
        {`${selectedWord ? `'${selectedWord.lexeme}'` : "No entry selected"} - Translations`}
      </h2>{" "}
      <div className="table-wrapper">
        <table className="styled-table">
          <thead>
            <tr>
              <th>No.</th>
              <th>Lexeme</th>
              <th>Category</th>
              <th>Pack</th>
              <th>Relation</th>
            </tr>
          </thead>
          <tbody>
            {translationsStatus === "idle" && (
              <tr className="status-row">
                <td className="status-row-cell" colSpan={5}>Select an entry to view its translations.</td>
              </tr>
            )}
            {translationsStatus === "loading" && (
              <tr className="status-row">
                <td className="status-row-cell" colSpan={5}>Loading translations...</td>
              </tr>
            )}

            {translationsStatus === "no-mappings" && (
              <tr className="status-row">
                <td colSpan={5} className="status-row-cell">
                  No translations are mapped to this entry yet.
                </td>
              </tr>
            )}

            {translationsStatus === "error" && (
              <tr>
                <td colSpan={5}>
                  Error loading translations: {translationsError}
                </td>
              </tr>
            )}

            {translationsStatus === "loaded" && translations.length === 0 && (
              // defensive: backend might return empty array instead of 404
              <tr>
                <td colSpan={4}>
                  No translations are mapped to this entry yet.
                </td>
              </tr>
            )}

            {translationsStatus === "loaded" &&
              translations.map((t, i) => (
                <tr
                  key={t.id}
                  onClick={(event) => onTranslationRowClick(event, t.id)}
                  className={
                    selectedTranslation?.id === t.id ? "selected-row" : ""
                  }
                >
                  <td data-label="No.">{i + 1}</td>
                  <td data-label="Lexeme">{t.lexeme}</td>
                  <td data-label="Category">{t.category ?? "-"}</td>
                  <td data-label="Pack">{t.wordpack ?? "-"}</td>
                  <td data-label="relation-type">{t.relation_type ?? "undefined"}</td>

                </tr>
              ))}
          </tbody>
        </table>
      </div>
      <div id="mts-control-panel" className="pvw-card-control-panel">
        <ButtonIconContainer
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 4.5v15m7.5-7.5h-15"
              />
            </svg>
          }
          label="Add Translation"
          onClick={onAddTranslation}
        ></ButtonIconContainer>

        <ButtonIconContainer
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              className="size-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
              />
            </svg>
          }
          label="Edit Translation"
          onClick={onEditTranslation}
        ></ButtonIconContainer>

        <ButtonIconContainer
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              className="size-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m6 4.125 2.25 2.25m0 0 2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"
              />
            </svg>
          }
          label="Delete Translation"
          onClick={onDeleteTranslation}
        ></ButtonIconContainer>
      </div>
      {newTranslationModalWindowMode !== "hidden" && (
        <NewTranslationModalWindow
          initialText={selectedTranslation?.lexeme}
          initialCategory={selectedTranslation?.category}
          initialPack={selectedTranslation?.wordpack}
          initialLangCode={selectedTranslation?.language_code}
          // initialRelationType={selectedTranslation}

          onCancel={() => {
            setNewTranslationModalWindowMode("hidden");
            // setTranslation(null);
          }}
          onAdd={
            newTranslationModalWindowMode === "adding"
              ? createTranslation
              : editTranslation
          }
        ></NewTranslationModalWindow>
      )}
    </section>
  );
}

export default TranslationPanel;
