import React, { useCallback, useEffect, useState } from "react";

import ButtonIconContainer from "../components/icon_slots/label_icon_container/ButtonIconContainer";
import InputIconContainer from "../components/icon_slots/input_icon_container/InputIconContainer";
import api, { USER_PREFIX, WORD_PREFIX } from "../api/api";
import { useAuth } from "../user_account/auth_context/AuthContext";
import type { ModalWindowMode } from "./PersonalVocabulary";
import {
  INITIAL_LEXEME,
  NewWordModalWindow,
} from "./modal_windows/new_entry_modal_window/NewEntryModalWindow";
import type { Word, WordCreate } from "../api/types";
import { edit_entry } from "./crud";
import { ConfirmDialog } from "./modal_windows/confirm_action_modal_window/ConfirmDialog";

type EntriesTableProps = {
  entries: Word[];
  setEntries: React.Dispatch<React.SetStateAction<Word[]>>;
  selectedEntryId: number | null;
  setSelectedEntryId: React.Dispatch<React.SetStateAction<number | null>>;
  selectedWord: Word | undefined;
  confirmActionMode?: ModalWindowMode;
  confirmActionMessage?: string;
  setConfirmActionMode?: React.Dispatch<React.SetStateAction<ModalWindowMode>>;
  setConfirmActionMessage?: React.Dispatch<React.SetStateAction<string>>;
  actionToConfirm?: () => void;
  setActionToConfirm?: React.Dispatch<React.SetStateAction<() => void>>;
};

export const EntriesTable = React.memo(function EntriesTable({
  entries,
  setEntries,
  selectedEntryId,
  setSelectedEntryId,
  selectedWord,
  confirmActionMode,
  confirmActionMessage,
  setConfirmActionMode,
  setConfirmActionMessage,
  actionToConfirm,
  setActionToConfirm,
}: EntriesTableProps) {
  const { user } = useAuth(); // call hook here, at top level of component
  const [loading, setLoading] = useState(true);
  const [newEntryModalWindowMode, setNewEntryModalWindowMode] =
    useState<ModalWindowMode>("hidden");

  const createEntry = async (newEntry: WordCreate) => {
    console.log("Word", newEntry);

    if (!user) {
      throw new Error("User must be logged in to create a word.");
    }

    try {
      const res = await api.post<Word>(WORD_PREFIX, newEntry);
      setEntries((prev) => [...prev, res.data]); // append to entries
      setNewEntryModalWindowMode("hidden");
    } catch (err) {
      console.error("Error creating word or user-word mapping:", err);
      throw err;
    }
  };

  const editEntry = async (entry: WordCreate) => {
    if (!user) {
      throw new Error("User must be logged in to create a word.");
    }

    if (!selectedEntryId) {
      throw new Error(
        "Unexpected: Editing triggered without selecting an entry first."
      );
    }

    await edit_entry(entry, selectedEntryId).then((res) => {
      const updatedWord = res.data;
      setEntries((prev) =>
        prev.map((word) => (word.id === updatedWord.id ? updatedWord : word))
      );
      setNewEntryModalWindowMode("hidden");
    });
  };

  const delete_entry = async (entry: Word) => {
    try {
      const res = await api.delete<Word>(`${WORD_PREFIX}/${entry.id}`);
      return res;
    } catch (err) {
      console.error("Error deleting word", err);
      throw err;
    }
  };

  const onClickAddEntry = () => {
    setNewEntryModalWindowMode("adding");
    console.log("Add Entry clicked");
  };

  const onClickEditEntry = () => {
    if (entries.length === 0) {
      alert("Please add a lexical entry first.");
      return;
    }

    if (selectedEntryId === null) {
      alert("Please select a lexical entry first.");
      return;
    }

    setNewEntryModalWindowMode("editing");
  };

  const onClickDeleteEntry = async () => {
    if (entries.length === 0) {
      alert("Please add a lexical entry first.");
      return;
    }

    if (selectedEntryId === null) {
      alert("Please select a lexical entry first.");
      return;
    }

    await delete_entry(entries.find((val) => val.id === selectedEntryId)!).then((res) => {
      setEntries((prev) => prev.filter((word) => word.id !== selectedEntryId));
      setSelectedEntryId(null);
    })
    
  };

  const onRowClick = useCallback((entry: Word) => {
    setSelectedEntryId(entry.id);
  }, []);

  useEffect(() => {
    if (user) {
      api
        .get<Word[]>(USER_PREFIX + "/me/words")
        .then((res) => {
          console.log("setting entries", res.data);
          setEntries(res.data);
        })
        .catch((err) => {
          console.error("Error fetching entries:", err);
          setLoading(false);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [user, newEntryModalWindowMode]);

  return (
    <section id="pvw-lexical-entries-section" className="pvw-card">
      <h2 className="section-title">Entries</h2>

      {loading ? (
        <p>Loading entries...</p>
      ) : entries.length === 0 ? (
        <p>No entries found.</p>
      ) : (
        <div className="table-wrapper">
        <div id="les-table" role="table" aria-label="Lexeme list">
          <div className="les-table-row" role="row">
            <div className="les-table-cell" role="columnheader">
              No.
            </div>
            <div className="les-table-cell" role="columnheader">
              Lexeme
            </div>

            <div className="les-table-cell" role="columnheader">
              Category
            </div>

            <div className="les-table-cell" role="columnheader">
              Pack
            </div>

            <div className="les-table-cell" role="columnheader">
              Lang
            </div>
            
          </div>
          {entries.map((entry, i) => (
            <EntryRow
              key={entry.id}
              entry={entry}
              index={i}
              onSelect={onRowClick}
              selected={entry.id === selectedEntryId}
            />
          ))}

        </div>
        </div>
        
      )}
      <InputIconContainer
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
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
              />
            </svg>
          }
          placeholder="Search entry"
          onChange={(e) => console.log("Input changed:", e.target.value)}
        />

      <div id="les-table-control-panel" className="pvw-card-control-panel">
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
          label="Add Word"
          onClick={() => onClickAddEntry()}
        />
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
          label="Edit Entry"
          onClick={() => onClickEditEntry()}
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
          label="Delete Entry"
          onClick={() => {
            setConfirmActionMode && setConfirmActionMode("editing")
            setConfirmActionMessage && setConfirmActionMessage("Are you sure you want to delete this entry?")
            setActionToConfirm && setActionToConfirm(() => onClickDeleteEntry);
          }}
        ></ButtonIconContainer>
      </div>
      {newEntryModalWindowMode !== "hidden" && (
        <NewWordModalWindow
          initialLexeme={
            newEntryModalWindowMode === "editing" && selectedWord
              ? selectedWord.lexeme
              : INITIAL_LEXEME
          }
          onCancel={() => {
            setNewEntryModalWindowMode("hidden");
          }}
          onAdd={
            newEntryModalWindowMode === "adding"
              ? async (newEntry) => {
                  createEntry(newEntry);
                }
              : async (entry) => {
                  editEntry(entry);
                }
          }
        ></NewWordModalWindow>
      )}

      {confirmActionMode === "editing" && (
        <ConfirmDialog
          message={confirmActionMessage ?? ""}
          onAdd={() => {
              if (actionToConfirm) actionToConfirm();
              if (setConfirmActionMode) setConfirmActionMode("hidden");
          }}
          onCancel={() => {
            if (setConfirmActionMode) setConfirmActionMode("hidden");
          }}
        ></ConfirmDialog>
      )}
    </section>
  );
});

const EntryRow = React.memo(function EntryRow({
  entry,
  index,
  onSelect,
  selected,
}: {
  entry: Word;
  index: number;
  onSelect: (entry: Word) => void;
  selected: boolean;
}) {
  const click = useCallback(() => onSelect(entry), [onSelect, entry.id]);
  return (
    <div
      className={`les-table-row ${selected ? "selected-row" : ""}`}
      role="row"
      onClick={click}
    >
      <div className="les-table-cell">{index + 1}</div>
      <div className="les-table-cell">{entry.lexeme}</div>
      <div className="les-table-cell">{entry.category}</div>
      <div className="les-table-cell">{entry.wordpack}</div>
      <div className="les-table-cell">{entry.language_code}</div>
    </div>
  );
});