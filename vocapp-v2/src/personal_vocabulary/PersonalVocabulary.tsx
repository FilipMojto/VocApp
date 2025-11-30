import "../styles/search_bar.css";
import "./styles/personal_vocabulary.css";
import "./styles/lexical_entries_section.css";
import "./styles/mapped_translations_section.css";

import { useEffect, useState } from "react";
import { useAuth } from "../user_account/auth_context/AuthContext";
import TranslationPanel from "./TranslationPanel";
import { EntriesTable } from "./EntriesTable";

interface Word {
  id: number;
  lexeme: string;
  category: string;
  wordpack: string;
  language_code: string;
}

export type ModalWindowMode = "hidden" | "adding" | "editing";


function PersonalVocabulary() {
  const { user } = useAuth();
  const [entries, setEntries] = useState<Word[]>([]);
  const [selectedEntryId, setSelectedEntryId] = useState<number | null>(null);
  const [selectedWord, setSelectedWord] = useState<Word>();

  const [confirmActionMode, setConfirmActionMode] = useState<ModalWindowMode>("hidden");
  const [confirmActionMessage, setConfirmActionMessage] = useState<string>("");
  const [actionToConfirm, setActionToConfirm] = useState<() => void>(() => {});
  
  useEffect(() => {
      if (selectedEntryId) {
        setSelectedWord(entries.find((e) => e.id === selectedEntryId));
      }
    }, [selectedEntryId]);

    
  if (!user) {
    return <label>Please log in to access your personal vocabulary.</label>;
  }

  return (
    <>
      <div id="personal-vocabulary-window">
        <header id="pvw-header">
          <h1>Personal Vocabulary</h1>
        </header>

        <main id="pvw-content-container">
          <EntriesTable
            entries={entries}
            setEntries={setEntries}
            selectedEntryId={selectedEntryId}
            setSelectedEntryId={setSelectedEntryId}
            selectedWord={selectedWord}
            confirmActionMode={confirmActionMode}
            setConfirmActionMode={setConfirmActionMode}
            confirmActionMessage={confirmActionMessage}
            setConfirmActionMessage={setConfirmActionMessage}
            actionToConfirm={actionToConfirm}
            setActionToConfirm={setActionToConfirm}
          />

          <TranslationPanel
            entries={entries}
            selectedWord={selectedWord}
          ></TranslationPanel>
        </main>
      </div>
    </>
  );
}

export default PersonalVocabulary;

