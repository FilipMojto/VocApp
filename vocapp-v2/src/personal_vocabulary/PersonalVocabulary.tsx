import "../styles/search_bar.css";
import "./styles/personal_vocabulary.css";
import "./styles/lexical_entries_section.css";
import "./styles/mapped_translations_section.css";

import { useCallback, useState } from "react";
import { useEffect } from "react";
import { useRef } from "react";
import InputIconContainer from "../components/icon_slots/input_icon_container/InputIconContainer";
import IconContainer from "../components/icon_slots/icon_container/IconContainer";
// import InputIconContainer from './components/icon_slots/input_icon_container/InputIconContainer'
import ButtonIconContainer from "../components/icon_slots/label_icon_container/ButtonIconContainer";
import { useAuth } from "../user_account/auth_context/AuthContext";
import api from "../api";
import NewTranslationModalWindow from "./new_translation_modal_window/NewTranslationModalWindow";
interface LexicalEntry {
  id: number;
  lexeme: string;
  // add other fields from your schemas if needed
}

interface Translation {
  id: number;
  lexeme: string;
  category: string;
  pack: string;
  // add other fields from your schemas if needed
}


function PersonalVocabulary() {
  const { user, setUser } = useAuth();
  const [entries, setEntries] = useState<LexicalEntry[]>([]);
  const [entries_loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<number | null>(null);


  // add these states near your other states
type TranslationsStatus = "idle" | "loading" | "no-mappings" | "error" | "loaded";
const [translations, setTranslations] = useState<Translation[]>([]);
const [translationsStatus, setTranslationsStatus] = useState<TranslationsStatus>("idle");
const [translationsError, setTranslationsError] = useState<string | null>(null);
const latestTranslationsReqId = useRef(0);


type NewTranslationModalWindowMode = "hidden" | "adding" | "editing";
const [newTranslationModalWindowMode, setNewTranslationModalWindowMode] = useState<NewTranslationModalWindowMode>("hidden");
const [translation, setTranslation] = useState<Translation | null>(null); // for editing existing translation

// updated handleRowClick with 404 handling
const handleRowClick = useCallback((entry: LexicalEntry) => {
  setSelectedId(entry.id);

  const reqId = ++latestTranslationsReqId.current;
  setTranslationsStatus("loading");
  setTranslationsError(null);

  api
    .get<Translation[]>(`/entry_translations/${entry.id}`)
    .then((res) => {
      if (reqId !== latestTranslationsReqId.current) return; // stale
      setTranslations(res.data ?? []);
      setTranslationsStatus("loaded");
    })
    .catch((err: any) => {
      if (reqId !== latestTranslationsReqId.current) return; // stale

      // axios-like error object: err.response.status
      const status = err?.response?.status;
      if (status === 404) {
        // backend signals "no translations" via 404
        setTranslations([]);
        setTranslationsStatus("no-mappings");
      } else {
        console.error("Error fetching translations:", err);
        setTranslations([]);
        setTranslationsStatus("error");
        setTranslationsError(err?.message ?? "Failed to load translations");
      }
    });
}, []);


  useEffect(() => {
    if (user) {
      api
        .get<LexicalEntry[]>("/users/me/entries") // backend should return list
        .then((res) => {
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
  }, [user]);

  const handleAddTranslation = () => {
    // logic to add a new lexical entry
    if (entries.length === 0) {
      alert("Please add a lexical entry first.");
      return;
    }

    setTranslation(null); // ensure no pre-filled data
    setNewTranslationModalWindowMode("adding");
    console.log("Add Translation clicked");

    
  }

  if (!user) {
    return <label>Please log in to access your personal vocabulary.</label>;
  }

  return (
    <>
      {/* {user && ( */}
        <div id="personal-vocabulary-window">
          <header id="pvw-header">
            <h1>Personal Vocabulary</h1>
          </header>

          <main id="pvw-content-container">
            <section id="pvw-lexical-entries-section" className="pvw-card">
              <h2 className="section-title">Entries</h2>

              {entries_loading ? (
                <p>Loading entries...</p>
              ) : entries.length === 0 ? (
                <p>No entries found.</p>
              ) : (
                <div id="les-table" role="table" aria-label="Lexeme list">
                  <div className="les-table-row" role="row">
                    <div className="les-table-cell" role="columnheader">
                      No.
                    </div>
                    <div className="les-table-cell" role="columnheader">
                      Lexeme
                    </div>
                  </div>

                  {entries.map((entry, index) => (
                    <div key={entry.id} className="les-table-row" role="row" onClick={() => handleRowClick(entry)}>
                      <div className="les-table-cell" role="cell">
                        {index + 1}
                      </div>
                      <div className="les-table-cell" role="cell">
                        {entry.lexeme}
                      </div>
                    </div>

                    
                  ))}
                </div>
              )}

              <div
                id="les-table-control-panel"
                className="pvw-card-control-panel"
              >

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
                  onChange={(e) =>
                    console.log("Input changed:", e.target.value)
                  }
                />

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
                  label="Add Entry"
                />
              </div>
            </section>

            <section
              id="pvw-mapped-translations-section"
              className="pvw-card table-card"
            >
              <h2 className="section-title">Mapped Translations</h2>
              <div className="table-wrapper">
                <table className="styled-table">
                  <thead>
                    <tr>
                      <th>No.</th>
                      <th>Lexeme</th>
                      <th>Category</th>
                      <th>Pack</th>
                    </tr>
                  </thead>
                  <tbody>
                    {translationsStatus === "loading" && (
                      <tr><td colSpan={4}>Loading translations...</td></tr>
                    )}

                    {translationsStatus === "no-mappings" && (
                      <tr>
                        <td colSpan={4}>
                          No translations are mapped to this entry yet.
                          {/* optionally add a small button/link to create a translation */}
                        </td>
                      </tr>
                    )}

                    {translationsStatus === "error" && (
                      <tr><td colSpan={4}>Error loading translations: {translationsError}</td></tr>
                    )}

                    {translationsStatus === "loaded" && translations.length === 0 && (
                      // defensive: backend might return empty array instead of 404
                      <tr><td colSpan={4}>No translations are mapped to this entry yet.</td></tr>
                    )}

                    {translationsStatus === "loaded" && translations.map((t, i) => (
                      <tr key={t.id}>
                        <td data-label="No.">{i + 1}</td>
                        <td data-label="Lexeme">{t.lexeme}</td>
                        <td data-label="Category">{t.category ?? "-"}</td>
                        <td data-label="Pack">{t.pack ?? "-"}</td>
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
                  onClick={() => handleAddTranslation()}
                  
                ></ButtonIconContainer>
                <ButtonIconContainer
                  icon={
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      className="size-6"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m6 4.125 2.25 2.25m0 0 2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"
                      />
                    </svg>
                  }
                  label="Delete Translation"
                ></ButtonIconContainer>
              </div>
            </section>
            {newTranslationModalWindowMode !== "hidden" && (
              <NewTranslationModalWindow
                onCancel={
                  () => {
                    setNewTranslationModalWindowMode("hidden");
                    setTranslation(null);
                  }
                  
                }
                onAdd={(newTranslation) => {
                  console.log("New translation to add:", newTranslation);
                  api.post<Translation>("/translations/", newTranslation)
                    .then((res) => {
                      api.post("/entry_translations/", {
                        entry_id: selectedId!,
                        translation_id: res.data.id
                      }).then(() => {

                          console.log("Translation added:", res.data);
                          setNewTranslationModalWindowMode("hidden");
                          setTranslation(null);
                          // Optionally refresh translations list if an entry is selected
                          if (selectedId) { handleRowClick(entries.find(e => e.id === selectedId)!);  // non-null assertion since selectedId is from entries
                        }});
                    })
                  
                }}></NewTranslationModalWindow>
            )}
          </main>
        </div>

    </>
  );
}

export default PersonalVocabulary;
