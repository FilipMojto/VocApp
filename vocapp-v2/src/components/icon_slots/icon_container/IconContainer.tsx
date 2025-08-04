// IconWrapper.tsx
import { forwardRef } from "react";
import "./icon_container.css";
// shared base
export interface BaseIconSlotProps {
  icon: React.ReactNode;
  containerClassName?: string;
  iconSlotClassName?: string;
}

export interface IconContainerProps extends BaseIconSlotProps, React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode; // slot for extension
}

const IconContainer = forwardRef<HTMLDivElement, IconContainerProps>(
  (
    {
      icon,
      containerClassName = "",
      iconSlotClassName = "",
      children,
      className,
      ...rest
    },
    ref
  ) => {
    return (
      <div
        ref={ref}
        className={`icon-container ${containerClassName} ${className || ""}`}
        {...rest}
      >
        <div className={`icon-slot ${iconSlotClassName}`} aria-hidden="true">
          {icon}
        </div>
        {children}
      </div>
    );
  }
);

export default IconContainer;