import type { RelationType } from "../personal_vocabulary/crud/WordRelation";

export interface Word {
  id: number;
  lexeme: string;
  language_code: string;
  category: string;
  wordpack: string;
}

export type WordCreate = Omit<Word, "id">;

export interface RelationEntry extends Word {
  relation_type: RelationType;
}


export interface UserWord{
    user_id: number;
    word_id: number;
}