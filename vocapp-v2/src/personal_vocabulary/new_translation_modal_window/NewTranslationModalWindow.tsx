import './NewTranslationModelWindow.css';
import { useState } from 'react';

export interface NewTranslationModalWindowProps {
  initialText?: string;
  initialCategory?: string;
  initialPack?: string;
  onCancel?: () => void;
  onAdd?: (payload: { lexeme: string; category: string; pack: string }) => void;
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
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleCancel = (e?: React.MouseEvent) => {
    e?.preventDefault();
    setError(null);
    onCancel ? onCancel() : console.log('Cancel new translation');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!text.trim()) {
      setError('Please enter the translation text.');
      return;
    }

    setSubmitting(true);
    const payload = {
        lexeme: text.trim(),
        category: (category ?? '').toString().toLowerCase(),
        pack:     (pack ?? '').toString().toLowerCase(),
    };

    try {
      // If caller provided onAdd, call it (could POST to backend there).
      if (onAdd) {
        await Promise.resolve(onAdd(payload));
      } else {
        // fallback behavior: just log
        console.log('Add translation (no onAdd provided):', payload);
      }
      // optionally reset fields:
      setText('');
      setCategory(initialCategory);
      setPack(initialPack);
    } catch (err: any) {
      setError(err?.message ?? 'Failed to add translation.');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div id="new-translation-modal-window" role="dialog" aria-labelledby="ntmw-title" aria-modal="true">
      <form className="ntmw-card" onSubmit={handleSubmit} noValidate>
        <header className="ntmw-header">
          <h2 id="ntmw-title">New Translation</h2>
        </header>

        <div className="ntmw-body">
          <label htmlFor="ntmw-text" className="ntmw-label">
            Translation
          </label>
          <input
            id="ntmw-text"
            className="ntmw-input"
            type="text"
            placeholder="Enter new translation…"
            value={text}
            onChange={(e) => setText(e.target.value)}
            aria-required="true"
            autoComplete="off"
          />

          <div className="ntmw-row">
            <div className="ntmw-field">
              <label htmlFor="ntmw-category" className="ntmw-label">
                Category
              </label>
              <select
                id="ntmw-category"
                className="ntmw-select"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="general">Neutral</option>
                <option value="work">Formal</option>
                <option value="travel">Informal</option>
                <option value="food">Idiomatic</option>
              </select>
            </div>

            <div className="ntmw-field">
              <label htmlFor="ntmw-pack" className="ntmw-label">
                Pack
              </label>
              <select
                id="ntmw-pack"
                className="ntmw-select"
                value={pack}
                onChange={(e) => setPack(e.target.value)}
              >
                <option value="default">Basic</option>
                <option value="advanced">Furniture</option>
              </select>
            </div>
          </div>

          {error && <div className="ntmw-error" role="status">{error}</div>}
        </div>

        <footer className="ntmw-footer">
          <button type="button" className="ntmw-btn ntmw-btn-ghost" onClick={handleCancel} disabled={submitting}>
            Cancel
          </button>
          <button type="submit" className="ntmw-btn ntmw-btn-primary" disabled={submitting}>
            {submitting ? 'Adding…' : 'Add'}
          </button>
        </footer>
      </form>
    </div>
  );
}

export default NewTranslationModalWindow;