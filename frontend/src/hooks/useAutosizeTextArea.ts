import { useEffect } from 'react';

export const useAutosizeTextArea = (textAreaRef: HTMLTextAreaElement | null, value: string) => {
    useEffect(() => {
        if (textAreaRef) {
            textAreaRef.style.height = "auto";
            const scrollHeight = textAreaRef.scrollHeight;
            textAreaRef.style.height = scrollHeight + "px";
        }
    }, [textAreaRef, value]);
};
