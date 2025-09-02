import './NewTranslationModelWindow.css';
import { useState } from 'react';



interface MLInputBase {
    // id?: string;
    label: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
    defaultValue?: string;
}

export interface MLInput extends MLInputBase {
    placeholder?: string;
}

export interface MLSelect extends MLInputBase {
    options?: { value: string; label: string }[];
}

export interface MLRow {
    fields: (MLInput | MLSelect)[];
}

interface ModalWindowFormProps {
    rows?: MLRow[];
    // viewportId?: string;
    // onSubmit?: () => void;
    onSubmit?: () => Promise<void>; // child provides the submit action
    // handleSubmit?: (e: React.FormEvent) => void;
    onCancel?: () => void;
    headerTitle?: string;
    // errorMessage?: string;
    // addButtonDisabled?: boolean;
}

export function ModalWindowForm({ rows, onSubmit, onCancel, headerTitle }: ModalWindowFormProps) {
    // const [text, setText] = useState(initialText);
    // const [category, setCategory] = useState(initialCategory);

    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);


    // const handleSubmit = async (e: React.FormEvent) => {
    //     e.preventDefault();
    //     setError(null);

    //     if (!text.trim()) {
    //     setError('Please enter the translation text.');
    //     return;
    //     }

    //     setSubmitting(true);
    //     const payload = {
    //         lexeme: text.trim(),
    //         category: (category ?? '').toString().toLowerCase(),
    //         pack:     (pack ?? '').toString().toLowerCase(),
    //     };

    //     try {
    //     // If caller provided onAdd, call it (could POST to backend there).
    //     if (onAdd) {
    //         await Promise.resolve(onAdd(payload));
    //     } else {
    //         // fallback behavior: just log
    //         console.log('Add translation (no onAdd provided):', payload);
    //     }
    //     // optionally reset fields:
    //     setText('');
    //     setCategory(initialCategory);
    //     setPack(initialPack);
    //     } catch (err: any) {
    //     setError(err?.message ?? 'Failed to add translation.');
    //     console.error(err);
    //     } finally {
    //     setSubmitting(false);
    //     }
    // };

    const handleCancel = (e?: React.MouseEvent) => {
        e?.preventDefault();
        setError(null);
        // onCancel ? onCancel() : console.log('Cancel new translation');
        onCancel ? onCancel() : console.log('Cancel new translation');

    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        if (!onSubmit) return;
        setSubmitting(true);

        await onSubmit().catch((err: any) => {
            setError(err?.message ?? 'Submission failed');
        }).finally(() => {
            setSubmitting(false);
        });
        // try {
        //     await onSubmit(); // child will do validation + network call
        // } catch (err: any) {
        //     setError(err?.message ?? 'Submission failed');
        // } finally {
        //     setSubmitting(false);
        // }
    };

    return (
        <div id="new-translation-modal-window" role='dialog' aria-labelledby='ntmw-title' aria-modal='true'>
            <form className="ntmw-card" onSubmit={handleSubmit} noValidate>
                <header className="ntmw-header">
                    <h2 id="ntmw-title">{headerTitle}</h2>
                </header>

                <div className="ntmw-body">
                    {rows?.map((row, rowIndex) => (
                        <div className="ntmw-row" key={`row-${rowIndex}`}>
                            {row.fields.map((field, fieldIndex) => (
                                <div className="ntmw-field" key={`field-${fieldIndex}`}>
                                    <label htmlFor='ntmw-text' className="ntmw-label">{field.label}</label>
                                    {'placeholder' in field ? (
                                        <input
                                            // id={field.id ?? `ntmw-input-${fieldIndex}`}
                                            id='ntmw-text'
                                            className="ntmw-input"
                                            type="text"
                                            placeholder={field.placeholder ?? ''}
                                            value={field.defaultValue ?? ''}
                                            onChange={field.onChange}
                                            aria-required="true"
                                            autoComplete="off"
                                        />
                                    ) : (
                                        <select
                                            // id={field.id ?? `ntmw-select-${fieldIndex}`}
                                            className="ntmw-select"
                                            value={field.defaultValue ?? ''}
                                            onChange={field.onChange}
                                        >
                                            {/* Example options; in real use, these would be dynamic or passed in */}
                                            {('options' in field ? field.options ?? [] : []).map((option, optIndex) => (
                                                <option key={`option-${optIndex}`} value={option.value}>
                                                    {option.label}
                                                </option>
                                            ))}
                                        </select>
                                    )}
                                </div>
                            ))}


                        </div>
                    ))}

                    {/* {errorMessage && <div className="ntmw-error" role="status">{errorMessage}</div>} */}
                    {(error) && <div className='ntmw-error' role="status">{error}</div>}

                </div>

                <footer className="ntmw-footer">
                    <button type="button" className="ntmw-btn ntmw-btn-ghost" onClick={handleCancel}>
                        Cancel
                    </button>
                    <button type="submit" className="ntmw-btn ntmw-btn-primary" disabled={ submitting}>
                        {submitting ? 'Adding…' : 'Add'}
                    </button>
                </footer>
            </form>
        </div>
    );
}

export interface ModalWindowBaseProps {
    onCancel?: () => void;
}

export interface NewTranslationModalWindowProps extends ModalWindowBaseProps {
    initialText?: string;
    initialCategory?: string;
    initialPack?: string;
    onAdd?: (payload: { lexeme: string; category: string; pack: string }) => void;

    // onCancel?: () => void;
    // onAdd?: (payload: { lexeme: string; category: string; pack: string }) => void;
    // optional: show/hide controlled externally if you want
}

function NewTranslationModalWindow({
    initialText = '',
    initialCategory = 'neutral',
    initialPack = 'basic',
    onCancel,
    onAdd,
}: NewTranslationModalWindowProps) {
    const [text, setText] = useState(initialText);
    const [category, setCategory] = useState(initialCategory);
    const [pack, setPack] = useState(initialPack);
    // const [error, setError] = useState<string | null>(null);
    // const [submitting, setSubmitting] = useState(false);

    // const handleCancel = (e?: React.MouseEvent) => {
    //     e?.preventDefault();
    //     setError(null);
    //     onCancel ? onCancel() : console.log('Cancel new translation');
    // };

    const submit = async () => {
        // e.preventDefault();
        // setError(null);

        if (!text.trim()) {
            // setError('Please enter the translation text.');
                //   throw new Error('Please enter the translation text.');

            return Promise.reject(new Error('Please enter the translation text.'));
            // return;
        }

        // setSubmitting(true);
        const payload = {
            lexeme: text.trim(),
            category: (category ?? '').toString().toLowerCase(),
            pack: (pack ?? '').toString().toLowerCase(),
        };

        // try {
        // If caller provided onAdd, call it (could POST to backend there).
        if (onAdd) {
            await Promise.resolve(onAdd(payload));
        } else {
            // fallback behavior: just log
            console.log('Add translation (no onAdd provided):', payload);
            // return Promise.resolve();
        }
        // optionally reset fields:
        setText('');
        setCategory(initialCategory);
        setPack(initialPack);
        // } catch (err: any) {
        //     setError(err?.message ?? 'Failed to add translation.');
        //     console.error(err);
        // } finally {
        //     setSubmitting(false);
        // }
        return Promise.resolve();
    };

    return (
        <ModalWindowForm
            // viewportId="new-translation-modal-window"
            headerTitle="New Translation"
            // handleSubmit={submit}
            // onCancel={handleCancel}
            onSubmit={submit}
            onCancel={onCancel}
            //
            // errorMessage={error ?? undefined}
            // addButtonDisabled={false}
            rows={[
                {
                    fields: [
                        { label: 'Translation', placeholder: 'Enter new translation…', defaultValue: text, onChange: (e) => setText(e.target.value) } as MLInput,
                    ]
                },
                {
                    fields: [
                        {
                            id: 'ntmw-category', label: 'Category', defaultValue: category, onChange: (e) => setCategory(e.target.value), options: [
                                { value: 'general', label: 'Neutral' },
                                { value: 'work', label: 'Formal' },
                                { value: 'travel', label: 'Informal' },
                                { value: 'food', label: 'Idiomatic' },
                            ]
                        } as MLSelect,
                        {
                            id: 'ntmw-pack', label: 'Pack', defaultValue: pack, onChange: (e) => setPack(e.target.value), options: [
                                { value: 'default', label: 'Basic' },
                                { value: 'advanced', label: 'Furniture' },
                            ]
                        } as MLSelect,
                    ]
                },
            ]}
        />
    );
}

export default NewTranslationModalWindow;