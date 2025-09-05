import React, { useRef, ChangeEvent, FormEvent } from 'react';
import { useAutosizeTextArea } from '../hooks/useAutosizeTextArea';

interface ChatInputProps {
    input: string;
    isLoading: boolean;
    handleInputChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
    handleSubmit: (e: FormEvent) => void;
    handleReset: () => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ input, isLoading, handleInputChange, handleSubmit, handleReset }) => {
    const textAreaRef = useRef<HTMLTextAreaElement>(null);
    useAutosizeTextArea(textAreaRef.current, input);

    return (
        <div className="chat-input-area">
            <button onClick={handleReset} className="new-convo-btn">New Conversation</button>
            <form onSubmit={handleSubmit} className="chat-input-form">
                <textarea
                    ref={textAreaRef}
                    value={input}
                    onChange={handleInputChange}
                    placeholder="I need to book an appointment for..."
                    disabled={isLoading}
                    rows={1}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                            e.preventDefault();
                            handleSubmit(e);
                        }
                    }}
                />
                <button type="submit" disabled={isLoading || !input.trim()}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M7 11L12 6L17 11M12 18V7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"></path></svg>
                </button>
            </form>
        </div>
    );
};

export default ChatInput;
