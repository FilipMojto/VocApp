import { useAuth } from "../../user_account/auth_context/AuthContext";
import api, { USER_WORD_PREFIX, WORD_PREFIX, WORD_RELATION_PREFIX } from "../../api/api";



export interface WordRelation {
    id: number;
    user_id: number;
    word_id: number;
    related_word_id: number;
    relation_type: string;
};

export type WordRelationCreate = Omit<WordRelation, "id">;

export const relationTypes = [
  "translation",
  "synonym",
  "antonym",
  "derived",
  "custom",
] as const;

export type RelationType = typeof relationTypes[number];

export function WordRelationCrud(){

    // const create = async (relation: WordRelation) => {
    //     try{
    //         const word_res = await api.get(`${WORD_PREFIX}/${relation.word_id}`);
    //         const related_word_res = await api.get(`${WORD_PREFIX}/${relation.related_word_id}`);

    //         const relation_res = await api.post<WordRelation>(WORD_PREFIX, relation);
            
    //         console.log("relation", relation.relation_type, "created successfully!");
    //         return relation_res;

    //         // handle successful response here
    //     } catch (error: any) {
    //         if (error.response && error.response.status === 404) {
    //             // handle 404 not found error
    //             throw new Error("Word/Related Word not found.");
    //             // console.error("Word not found.");
    //         } else {
    //             // rethrow or handle other errors
    //             throw error;
    //         }
    //     }
    // }

    // const get_translations = async (word_id: number, relation_type: RelationType = 'translation') => {
    //     // if (!user) {
    //     //     throw new Error("User must be logged in to create a word.");
    //     // }

    //     try{
    //         const response = await api.get<Word[]>(WORD_RELATION_PREFIX, {
    //             params: {
    //                 word_id,
    //                 relation_type,
    //             }
    //         })

    //         return response.data;
    //     }
    //     catch (error: any){
    //         console.log("Error fetching translations:", error);
    //         throw error;
    //     }
    // }
    
    // return {create};
}

