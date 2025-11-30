import api, { WORD_PREFIX } from "../../api/api";
import type { Word } from "../../api/types";
import { useAuth } from "../../user_account/auth_context/AuthContext";


// export interface Word {
//   id: number;
//   lexeme: string;
//   language_code: string;
//   category: string;
//   wordpack: string;
// }

// export type WordCreate = Omit<Word, "id">;


export function WordCRUD(){
    // const {user} = useAuth();

    // const createWord = async (newWord: WordCreate) => {
    //     console.log("Word", newWord);

    //     if (!user) {
    //         throw new Error("User must be logged in to create a word.");
    //     }

    //     try{
    //         const res = await api.post<Word>(WORD_PREFIX, newWord);
    //         return res.data;            
    //     }
    //     catch(err){
    //         console.error("Error creating word or user-word mapping:", err);
    //         throw err;
    //     }
    //     // try {
    //     //     // create global word
    //     //     const res = await api.post<Word>(WORD_PREFIX, newWord);
    //     //     const created = res.data;

    //     //     // link user -> word (users_words)
    //     //     const userWordPayload: Omit<WordRelation, "id"> = {
    //     //         user_id: user.id,
    //     //         word_id: created.id,
    //     //     };

    //     //     // POST mapping; await to propagate errors if mapping fails
    //     //     await api.post<WordRelation>(`${USER_WORD_PREFIX}/`, userWordPayload);

    //     //     return created;
    //     //     } catch (err) {
    //     //         console.error("Error creating word or user-word mapping:", err);
    //     //         throw err;
    //     //     }

    //     // console.log("Word", newWord);
        
    //     // api.post<Word>(WORD_PREFIX, newWord)
    //     // .then((res) => {
            
    //     //     const user_word_payload: Omit<WordRelation, "id"> = {
    //     //         user_id: user.id,
    //     //         word_id: res.data.id,
    //     //     }

    //     //     api.post<WordRelation>(USER_WORD_PREFIX + "/", user_word_payload)
    //     // })
    //     // .catch((err) => {
    //     //     console.log("Error creating word or userword:", err)
    //     //     throw err
    //     // })

        
    // };

    // const loadWords = async () => {
    //     // if (!user) {
    //     //     throw new Error("User must be logged in to create a word.");
    //     // }

    //     // api.get(USER_WORD_PREFIX + "/me/words")
    //     // .then((res) => {
    //     //     console.log("setting entries", res.data);
    //     // })
    //     // .catch((err) => {
    //     //   console.error("Error fetching entries:", err);
    //     //   setLoading(false);
    //     // })
    // }

    // const getTranslations = async () => {
    //     if (!user) {
    //         throw new Error("User must be logged in to create a word.");
    //     }

    //     api.get(WORD_PREFIX + "/translations")
    //     .then((res) => {

    //     })

        
    // }

    // return { createWord };
}

// export const createWord = (newWord: Word) => {
//     console.log("HEREs");
//     const {user} = useAuth();
//     console.log("HERE");


//      if (!user) {
//         throw new Error("User must be logged in to create a word.");
//     }
    
//     api.post<Word>(WORD_PREFIX, newWord)
//     .then((res) => {
        
//         const user_word_payload: Omit<UserWord, "id"> = {
//             user_id: user.id,
//             word_id: res.data.id,
//         }

//         api.post<UserWord>(USER_WORD_PREFIX + "/", user_word_payload)
//     })
//     .catch((err) => {
//         console.log("Error creating word or userword:", err)
//         throw err
//     })
// }

export const readWord = () => {

}

export const updateWord = () => {

}

export const deleteWord = () => {

}