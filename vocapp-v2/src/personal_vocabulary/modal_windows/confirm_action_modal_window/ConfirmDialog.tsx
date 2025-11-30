import './ConfirmDialog.css'

import { VocapModalWindow, type ModalWindowBaseProps, type VocapModalWindowForm } from "../base";


export interface ConfirmDialogProps extends ModalWindowBaseProps {
    message: string;
}

export interface ConfirmDialogProps extends VocapModalWindowForm {
}

export function ConfirmDialog({message, onAdd, onCancel}: ConfirmDialogProps) {
  const onSubmit = async () => {
    if (onAdd) {
        // const payload = {};
        await Promise.resolve(onAdd({}));
    } else {
        console.log("No onAdd handler provided.");
    }
    return Promise.resolve();
}
  
    return (
    <VocapModalWindow
        headerTitle="Confirm Action"
        onSubmit={onSubmit}
        onCancel={onCancel}
    >
        <p className="confirm-dialog-message">{message}</p>
    
    </VocapModalWindow>
    );
}