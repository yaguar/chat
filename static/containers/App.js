
import FormAdd from './FormAdd.js';
import React from 'react';
import ContactList from './ContactList';
import 'react-chat-elements/dist/main.css';
import { MessageBox, ChatItem, ChatList } from 'react-chat-elements';

const App = () => (
      <div>
	<FormAdd />
	<ContactList />
	<span width="30"><ChatItem
    avatar={'https://facebook.github.io/react/img/logo.svg'}
    alt={'Reactjs'}
    title={'Facebook'}
    subtitle={'What are you doing?'}
    date={new Date()}
    unread={2} /></span>
          <ChatList
    className='chat-list'
    dataSource={[
        {
            avatar: 'https://facebook.github.io/react/img/logo.svg',
            alt: 'Reactjs',
            title: 'Facebook',
            subtitle: 'What are you doing?',
            date: new Date(),
            unread: 0,
        },
    ]} />
	<MessageBox
    position={'left'}
    type={'text'}
    text={'sdfsdfsdfsdfdsfsdf'}
    data={{
        uri: 'https://facebook.github.io/react/img/logo.svg',
        status: {
            click: false,
            loading: 0,
        }
    }}/>
      </div>
);

export default App;
