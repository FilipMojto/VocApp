import IconContainer, { type BaseIconSlotProps } from '../icon_container/IconContainer';
import './button_icon_container.css';
import { forwardRef } from "react";

export interface LabeledContainerProps extends BaseIconSlotProps {
  label: string;
  labelClassName?: string;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
}

const ButtonIconContainer = forwardRef<HTMLButtonElement, LabeledContainerProps>(
  (
    {
      icon,
      label,
      containerClassName = "",
      iconSlotClassName = "",
      labelClassName = "",
      onClick,
      ...rest
    },
    ref
  ) => {
    const handleButtonClick: React.MouseEventHandler<HTMLButtonElement> = (e) => {
      // Run user-provided click handler if any
      if (onClick) {
        onClick(e);
      }

      // Example: prevent double-click text selection
      e.preventDefault();

      // You could also handle default button behavior here if needed
    };

    return (
      <button
        ref={ref}
        className={`labeled-icon-container ${containerClassName}`}
        onClick={handleButtonClick}
        type="button"
        {...rest}
      >
        <div className={`icon-slot ${iconSlotClassName}`} aria-hidden="true">
          {icon}
        </div>
        <span className={labelClassName}>{label}</span>
      </button>
    );
  }
);

export default ButtonIconContainer;