import '../new_translation_modal_window/NewTranslationModelWindow.css';

import { useState } from 'react';
import { ModalWindowForm, type MLInput, type ModalWindowBaseProps } from '../new_translation_modal_window/NewTranslationModalWindow';




interface NewEntryModalWindowState extends ModalWindowBaseProps {
    initialLexeme?: string;
    onAdd: (payload: { lexeme: string }) => void | Promise<void>;
}

export function NewEntryModalWindow({ initialLexeme = '', onAdd, onCancel }: NewEntryModalWindowState) {
    const [lexeme, setLexeme] = useState(initialLexeme);

    const submit = async () => {
        if (!lexeme.trim()) {
            return Promise.reject(new Error('Please enter the lexeme.'));
        }

        const payload = {
            lexeme: lexeme.trim(),
        };

        if (onAdd) {
            await Promise.resolve(onAdd(payload));
        } else {
            // return Promise.reject(new Error('No onAdd handler provided.'));
            console.log('No onAdd handler provided.');
        }

        setLexeme('');
        return Promise.resolve();
    }
    
    return (
        <ModalWindowForm
            // viewportId="new-translation-modal-window"
            
            headerTitle="Add New Lexical Entry"
            onSubmit={submit}
            onCancel={onCancel}
            rows={[
                {
                    fields: [
                        { label: 'Lexeme', placeholder: 'Enter new lexeme…', defaultValue: lexeme, onChange: (e) => setLexeme(e.target.value) } as MLInput,
                    ]
                }
            ]}
            // addButtonDisabled={false}

        ></ModalWindowForm>
        // <ModalWindowForm
        //     viewportId="new-entry-modal-window-viewport"
            
        //     headerTitle="Add New Lexical Entry"
        //     initialLexeme={initialLexeme}
        //     handleCancel={onCancel}
        //     handleSubmit={onAdd}
        //     // err
        // ></ModalWindowForm>

    )
}
