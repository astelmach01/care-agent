import React from 'react';
import ReactMarkdown from 'react-markdown';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatMessageProps {
    message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
    return (
        <div className={`message-wrapper ${message.role}`}>
            {message.role === 'assistant' && (
                <div className="assistant-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5C12.41 2.5 12.75 2.84 12.75 3.25V5.5C12.75 5.91 12.41 6.25 12 6.25C11.59 6.25 11.25 5.91 11.25 5.5V3.25C11.25 2.84 11.59 2.5 12 2.5ZM5.5 11.25H3.25C2.84 11.25 2.5 11.59 2.5 12C2.5 12.41 2.84 12.75 3.25 12.75H5.5C5.91 12.75 6.25 12.41 6.25 12C6.25 11.59 5.91 11.25 5.5 11.25ZM20.75 11.25H18.5C18.09 11.25 17.75 11.59 17.75 12C17.75 12.41 18.09 12.75 18.5 12.75H20.75C21.16 12.75 21.5 12.41 21.5 12C21.5 11.59 21.16 11.25 20.75 11.25ZM12 17.75C11.59 17.75 11.25 18.09 11.25 18.5V20.75C11.25 21.16 11.59 21.5 12 21.5C12.41 21.5 12.75 21.16 12.75 20.75V18.5C12.75 18.09 12.41 17.75 12 17.75ZM8.46 8.46C8.79 8.14 9.31 8.14 9.63 8.46C9.95 8.79 9.95 9.31 9.63 9.63L8.12 11.14C7.8 11.46 7.28 11.46 6.96 11.14C6.64 10.82 6.64 10.3 6.96 9.98L8.46 8.46ZM16.04 15.04C16.36 14.72 16.88 14.72 17.2 15.04C17.52 15.36 17.52 15.88 17.2 16.2L15.69 17.71C15.37 18.03 14.85 18.03 14.53 17.71C14.21 17.39 14.21 16.87 14.53 16.55L16.04 15.04ZM15.04 9.63C14.72 9.95 14.72 10.47 15.04 10.79L16.55 12.3C16.87 12.62 17.39 12.62 17.71 12.3C18.03 11.98 18.03 11.46 17.71 11.14L16.2 9.63C15.88 9.31 15.36 9.31 15.04 9.63ZM9.98 15.04C9.66 14.72 9.14 14.72 8.82 15.04L7.31 16.55C6.99 16.87 6.99 17.39 7.31 17.71C7.63 18.03 8.15 18.03 8.47 17.71L9.98 16.2C10.3 15.88 10.3 15.36 9.98 15.04Z" fill="currentColor"></path></svg>
                </div>
            )}
            <div className="message-content">
                <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
        </div>
    );
};

export default ChatMessage;
