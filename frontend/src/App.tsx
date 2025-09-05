import { useState, useRef, FormEvent, useEffect, ChangeEvent } from 'react';
import Header from './components/Header';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleReset = async () => {
    try {
      await fetch(`${API_BASE_URL}/reset`, { method: 'POST' });
      setMessages([]);
    } catch (error) {
      console.error("Error resetting conversation:", error);
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('prompt', input);

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const assistantMessage = await response.json();
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error("Error during chat submission:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, an error occurred.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <Header />
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput
        input={input}
        isLoading={isLoading}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
        handleReset={handleReset}
      />
    </div>
  );
}

export default App;