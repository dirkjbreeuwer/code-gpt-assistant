import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, List, ListItem, ListItemText, InputAdornment } from '@mui/material';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    const message = { text: input, user: 'user' };
    setMessages([...messages, message]);
    setInput('');

    const formattedInput = input.replace(/\n/g, '\\n');

    const response = await axios.post('http://127.0.0.1:5000/ask', { question: formattedInput });
    const botMessage = { text: response.data.answer, user: 'bot' };
    setMessages([...messages, message, botMessage]);
  };

  return (
    <div className="chat-container">
      <div className="chat-list">
        <List>
          {messages.map((message, index) => (
            <ListItem key={index} style={{ backgroundColor: message.user === 'user' ? '#ffffff' : '#f5f5f5', borderRadius: '5px', margin: '10px 0' }}>
            <ListItemText 
              primary={<span style={{ fontSize: '0.9rem', color: '#333' }} dangerouslySetInnerHTML={{ __html: message.text.replace(/\n/g, '<br />') }} />} 
              secondary={message.user} 
            />
          </ListItem>
          
          
          ))}
        </List>
      </div>
      <div className="chat-input">
        <TextField
          id="outlined-basic"
          label="Ask a question"
          variant="outlined"
          value={input}
          onChange={e => setInput(e.target.value)}
          multiline
          fullWidth
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <Button variant="contained" color="primary" onClick={sendMessage}>
                  Send
                </Button>
              </InputAdornment>
            ),
          }}
        />
      </div>
    </div>
  );
};

export default Chat;
