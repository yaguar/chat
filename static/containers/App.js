import React from 'react';
import 'react-chat-elements/dist/main.css';
import { MessageBox, ChatItem, ChatList } from 'react-chat-elements';
import SearchField from "react-search-field";
import addMessage from '../action/addmessage';
import rewriteMessages from '../action/rewritemessages';
import rewriteDialogs from '../action/rewritedialogs';
import Input from '../components/Input';
import {connect} from "react-redux";
import deleteMessage from "../action/deletemessage";
import {store} from "../index";

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

    };

    onChange(value) {
        let url = '/login_list?q=' + value
        fetch(url, {
                method: 'get', headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                }
            })
            .then(
                function (response) {
                    if (response.status != 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                            response.status);
                        return 0;
                    }
                    response.json().then(function(data) {
                        store.dispatch(rewriteDialogs(data))
                    });
                    return 1;

                }
            )
            .catch(function (err) {
                console.log('Fetch Error :-S', err);
            });
    }

    render () {
        return (
            <div>
                <div class="row">
                    <div class="col-sm-3">
                        <SearchField
                          placeholder="Search..."
                          onChange={this.onChange}
                        />
                        {this.props.dialogs.map((dlg, index) => (
                            <ChatItem
                                avatar={'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg'}
                                alt={'Reactjs'}
                                title={dlg.login}
                                subtitle={'not status'}
                                unread={0}
                                onClick={()=>this.props.rewriteMsg(dlg.id)}
                            />
                        ))}
                    </div>
                    <div className="col-sm-9">
                        <div style={{overflow:"scroll", height:"65%", overflowX:"hidden"}}>
                            {this.props.messages.map((msg, index) => (
                                <MessageBox
                                    key={index}
                                    position={msg.user === 'admin' ? 'right' : 'left'}
                                    type={'text'}
                                    text={msg.msg}
                                    index={index}
                                    date={new Date(msg.time)}
                                />
                            ))}
                        </div>
                    <span style={{position:"fixed", bottom:0, height:"25%", width:"60%", background:"white"}}>
                    <Input />
                    </span>
                    </div>
                </div>
            </div>
        );
    }
};

const mapDispatchToProps = (dispatch) => {
	return {
	    addMsg: (message) => {dispatch(addMessage(message))},
        rewriteDlg: (dialogs) => {dispatch(rewriteDialogs(dialogs))},
        rewriteMsg: (chat_id) => {
	        fetch('/messages/' + chat_id)
            .then(
            function(response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                    response.status);
                    return;
                }

                response.json().then(function(data) {
                    dispatch(rewriteMessages(data))
                });
            }
            )
            .catch(function(err) {
            console.log('Fetch Error :-S', err)
            })
	    }
	}
}

const mapStateToProps = (state) => {
	let props = {
		messages: state.messages.messages,
        dialogs: state.dialogs.dialogs,
	};
	return props;
}

const mainApp = connect(
	mapStateToProps,
    mapDispatchToProps
)(App);

export default mainApp;
