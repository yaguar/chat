
import React from 'react';
import 'react-chat-elements/dist/main.css';
import { MessageBox, ChatItem, ChatList } from 'react-chat-elements';
import addMessage from '../action/addmessage';
import Input from '../components/Input';
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

            this.props.addMsg(JSON.parse(evt.data))
        }

    }

    render () {
        return (
<div>
    {this.props.messages.map((msg, index) => (
        <MessageBox
            key={index}
            position={msg.user === 'admin' ? 'right' : 'left'}
            type={'text'}
            text={msg.msg}
            index={index}
            date={new Date(msg.time)}
            data={{
                uri: 'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg',
                    status: {
                        click: false,
                        loading: 0,
                    }
            }}
        />
    ))}
    <br/>
    <Input />

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
