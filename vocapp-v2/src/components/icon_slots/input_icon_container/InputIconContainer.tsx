// import '../icon_container/icon_container.css';
import './input_icon_container.css';

// InputIconContainer.tsx
import {
  forwardRef,
  useId,
  useMemo,
  useState,
  useEffect,
  type ChangeEvent,
} from "react";
import IconContainer from "../icon_container/IconContainer"; // adjust path
// import "./input_icon.css";
import type { BaseIconSlotProps } from "../icon_container/IconContainer";
// impor tkkfd "./input_icon_container.css"; // adjust path
export interface InputIconContainerProps
  extends BaseIconSlotProps, Omit<React.InputHTMLAttributes<HTMLInputElement>, "className"> {
//   icon: React.ReactNode;
  clearable?: boolean;
//   containerClassName?: string;
  inputClassName?: string;
//   iconContainerClassName?: string;
  onClear?: () => void;
}

const InputIconContainer = forwardRef<HTMLInputElement, InputIconContainerProps>(
  (
    {
      icon,
      clearable = true,
      containerClassName = "",
      inputClassName = "",
      iconSlotClassName: iconContainerClassName = "",
      onClear,
      value,
      defaultValue,
      onChange,
      ...rest
    },
    ref
  ) => {
    const generatedId = useId();
    const [internalValue, setInternalValue] = useState<string>(
      typeof value === "string"
        ? value
        : typeof defaultValue === "string"
        ? defaultValue
        : ""
    );

    // Sync controlled value
    useEffect(() => {
      if (typeof value === "string") {
        setInternalValue(value);
      }
    }, [value]);

    const showClear = useMemo(() => {
      return clearable && internalValue.length > 0;
    }, [clearable, internalValue]);

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
      if (onChange) onChange(e);
      if (value === undefined) {
        setInternalValue(e.target.value);
      }
    };

    const handleClear = () => {
      if (value === undefined) {
        setInternalValue("");
      }
      if (onClear) onClear();
      const synthetic = {
        target: { value: "" },
      } as unknown as ChangeEvent<HTMLInputElement>;
      if (onChange) onChange(synthetic);
      // focus back
      (ref as any)?.current?.focus?.();
    };

    return (
      <IconContainer
        icon={icon}
        containerClassName={"input-icon-container " + containerClassName}
        iconSlotClassName={iconContainerClassName}
        // style={{ width: "300px"}}
        // style={{ display: "flex", alignItems: "center", flexDirection: "row" }}
      >

        <input
          id={generatedId}
          ref={ref}
          className={`text-input ${inputClassName}`}
          value={internalValue}
          // style={{ flex: 1, minWidsdth: "500px" }}
          onChange={handleChange}
          {...rest}
        />
        {showClear && (
          <button
            type="button"
            aria-label="Clear"
            className="clear-button"
            onClick={handleClear}
          >
            &times;
          </button>
        )}
      </IconContainer>
    );
  }
);

export default InputIconContainer;