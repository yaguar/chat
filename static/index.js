import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import {createStore, combineReducers, getState} from 'redux';
import {applyMiddleware, compose} from 'redux';
import logger from 'redux-logger';
import {Component} from 'react';
import thunk from 'redux-thunk';
import addMessage from './action/addmessage';
import addMainInfo from './action/addmaininfo';
import rewriteDialogs from './action/rewritedialogs';
import App from './containers/App';
import messages from './reducers/messages';
import dialogs from './reducers/dialogs';
import main_info from './reducers/main_info';
import active_chat from './reducers/active_chat';

const rootReducer = combineReducers({
    messages: messages,
    dialogs: dialogs,
    main_info: main_info,
    active_chat: active_chat
});
 
export let store = createStore(
  rootReducer,
  compose(
    applyMiddleware(thunk),
    applyMiddleware(logger)
  ), 
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

fetch('/main_info')
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
        response.status);
        return;
      }

      response.json().then(function(data) {
        store.dispatch(addMainInfo(data))
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err)
  })

fetch('/messages')
  .then(  
    function(response) {  
      if (response.status !== 200) {  
        console.log('Looks like there was a problem. Status Code: ' +  
        response.status);  
        return;  
      }
 
      response.json().then(function(data) {  
        data.map((message, index) => store.dispatch(addMessage(message)))
      });  
    }  
  )  
  .catch(function(err) {  
    console.log('Fetch Error :-S', err) 
  })

fetch('/login_list?q=')
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
        response.status);
        return;
      }

      response.json().then(function(data) {
        store.dispatch(rewriteDialogs(data))
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err)
  })

ReactDOM.render(
  <Provider store={store}>
    <App />	
  </ Provider>,
  document.getElementById('root')
);

