import api, { WORD_PREFIX } from "../api/api";
import type { Word, WordCreate } from "../api/types";

export const edit_entry = async (entry: WordCreate, id: number) => {

    try {
      const res = await api.patch<Word>(
        `${WORD_PREFIX}/${id}`,
        entry
      );

      return res;
    //   setEntries((prev) =>
    //     prev.map((word) => (word.id === updatedWord.id ? updatedWord : word))
    //   );
    //   setNewEntryModalWindowMode("hidden");
    } catch (err) {
      console.error("Error updating word", err);
      throw err;
    }
  };