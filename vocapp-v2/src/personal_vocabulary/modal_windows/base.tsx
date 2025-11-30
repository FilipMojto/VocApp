import { useEffect, useState } from "react";

interface MLInputBase {
  label: string;
  onChange?: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
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
  onSubmit?: () => Promise<void>;
  onCancel?: () => void;
  headerTitle?: string;
  children?: React.ReactNode;
}

export interface VocapModalWindowForm{

}

export function VocapModalWindow({
  rows,
  onSubmit,
  onCancel,
  headerTitle,
  children,
}: ModalWindowFormProps) {
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleCancel = (e?: React.MouseEvent) => {
    e?.preventDefault();
    setError(null);
    onCancel ? onCancel() : console.log("Cancel new translation");
  };

  const handleSubmit = async (e?: React.FormEvent | KeyboardEvent) => {
    if (e && "preventDefault" in e && typeof e.preventDefault === "function") {
      e.preventDefault();
    }
    setError(null);
    if (!onSubmit) return;
    setSubmitting(true);

    await onSubmit()
      .catch((err: any) => {
        setError(err?.message ?? "Submission failed");
      })
      .finally(() => {
        setSubmitting(false);
      });
  };

   // Global Enter shortcut inside the modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      console.log("Key down:", e.key);
      if (e.key === "Enter" && !submitting) {
        // avoid double-submit if focused in textarea in the future
        if ((e.target as HTMLElement).tagName !== "TEXTAREA") {
          handleSubmit(e);
        }
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handleSubmit, submitting]);

  return (
    <div
      id="new-translation-modal-window"
      role="dialog"
      aria-labelledby="ntmw-title"
      aria-modal="true"
    >
      <form className="ntmw-card" onSubmit={handleSubmit} noValidate>
        <header className="ntmw-header">
          <h2 id="ntmw-title">{headerTitle}</h2>
        </header>

        <div className="ntmw-body">
          {rows?.map((row, rowIndex) => (
            <div className="ntmw-row" key={`row-${rowIndex}`}>
              {row.fields.map((field, fieldIndex) => (
                <div className="ntmw-field" key={`field-${fieldIndex}`}>
                  <label htmlFor="ntmw-text" className="ntmw-label">
                    {field.label}
                  </label>
                  {"placeholder" in field ? (
                    <input
                      id="ntmw-text"
                      className="ntmw-input"
                      type="text"
                      placeholder={field.placeholder ?? ""}
                      value={field.defaultValue ?? ""}
                      onChange={field.onChange}
                      aria-required="true"
                      autoComplete="off"
                    />
                  ) : (
                    <select
                      className="ntmw-select"
                      value={field.defaultValue ?? ""}
                      onChange={field.onChange}
                    >
                      {/* Example options; in real use, these would be dynamic or passed in */}
                      {("options" in field ? field.options ?? [] : []).map(
                        (option, optIndex) => (
                          <option
                            key={`option-${optIndex}`}
                            value={option.value}
                          >
                            {option.label}
                          </option>
                        )
                      )}
                    </select>
                  )}
                </div>
              ))}
            </div>
          ))}

          {error && (
            <div className="ntmw-error" role="status">
              {error}
            </div>
          )}
          {children}
        </div>

        <footer className="ntmw-footer">
          <button
            type="button"
            className="ntmw-btn ntmw-btn-ghost"
            onClick={handleCancel}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="ntmw-btn ntmw-btn-primary"
            disabled={submitting}
          >
            {submitting ? "Processing..." : "Confirm"}
          </button>
        </footer>
      </form>
    </div>
  );
}

export interface ModalWindowBaseProps {
  onCancel?: () => void;
  onAdd?: (payload: VocapModalWindowForm) => void;
}