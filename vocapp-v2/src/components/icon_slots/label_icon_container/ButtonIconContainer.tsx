// import './label_icon.css'

import IconContainer, { type BaseIconSlotProps } from '../icon_container/IconContainer';
import './button_icon_container.css';

// LabeledIcon.tsx
import { forwardRef } from "react";

export interface LabeledContainerProps extends BaseIconSlotProps {
//   icon: React.ReactNode;
  label: string;
//   containerClassName?: string;
//   iconContainerClassName?: string;
  labelClassName?: string;
}

// const ButtonIconContainer = forwardRef<HTMLDivElement, LabeledContainerProps>(
//   (
//     {
//       icon,
//       label,
//       containerClassName = "",
//       iconSlotClassName: iconContainerClassName = "",
//       labelClassName = "",
//       ...rest
//     },
//     ref
//   ) => {
//     return (
//       <IconContainer
//         ref={ref}
//         icon={icon}
//         containerClassName={"labeled-icon-container secondary" + " " + containerClassName}
//         iconSlotClassName={"bic-icon-slot" + " " + iconContainerClassName}
        
//         {...rest}
//       >
//         <button className={"bic-label" + " " + labelClassName}>{label}</button>
//       </IconContainer>
//     );
//   }
// );

const ButtonIconContainer = forwardRef<HTMLButtonElement, LabeledContainerProps>(
  (
    {
      icon,
      label,
      containerClassName = "",
      iconSlotClassName = "",
      labelClassName = "",
      ...rest
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={`labeled-icon-container ${containerClassName}`}
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