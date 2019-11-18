
import FormAdd from './FormAdd.js';
import React from 'react';
import ContactList from './ContactList';
import 'react-chat-elements/dist/main.css';
import { MessageBox, ChatItem, ChatList } from 'react-chat-elements';
import addMessage from '../action/addmessage';
import {connect} from "react-redux";
import deleteMessage from "../action/deletemessage";

class App extends React.Component {

    componentDidMount() {
        let ws = new WebSocket('ws://127.0.0.1:8000/ws')
        ws.onopen = () => {
        // on connecting, do nothing but log it to the console
        console.log('connected')
        }

        ws.onmessage = evt => {
            // console.log(this)

            this.props.addMsg(JSON.parse(evt.data))
        // listen to data sent from the websocket server
        }

        // ws.onclose = () => {
        // console.log('disconnected')
        // automatically try to reconnect on connection loss

        // }

    }

    render () {
        return (
<div>
<FormAdd />
<ContactList />
<span width="30"><ChatItem
avatar={'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg'}
alt={'Reactjs'}
title={'Facebook'}
subtitle={'What are you doing?'}
date={new Date()}
unread={2} /></span>
<ChatList
className='chat-list'
dataSource={[
    {
        avatar: 'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg',
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
    uri: 'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg',
    status: {
        click: false,
        loading: 0,
    }
}}/>
</div>);
    }
};

const mapDispatchToProps = (dispatch) => {
	return {addMsg: (message) => {dispatch(addMessage(message))} }
}

const mapStateToProps = (state) => {
	let props = {
		messages: state.messages.messages,
	};
	return props;
}

const mainApp = connect(
	mapStateToProps,
    mapDispatchToProps
)(App);

export default mainApp;
