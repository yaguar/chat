import {connect} from 'react-redux';
import React, {Component} from 'react';
import deleteMessage from '../action/deletemessage';
import Person from '../components/Person';

const App = ({messages, onClicker}) => 	(
  <ul class="list-group">
    {messages.map((message, index) => (
      <Person key={index} message={message} onClicker={onClicker} index={index}/>
    ))}
  </ul>
);

function method_delete(number){
  fetch('/listcontact', {method:'delete',headers: {
     'Accept': 'application/json, text/plain, */*',
     'Content-Type': 'application/json'
    }, body:JSON.stringify({
          number
      })})  
    .then(  
      function(response) {  
        if (response.status != 204){  
          console.log('Looks like there was a problem. Status Code: ' +  
            response.status);  
          return 0;  
        }

      // Examine the text in the response  
        
        return 1;  
          
      }  
    )  
    .catch(function(err) {  
      console.log('Fetch Error :-S', err);  
    });
}

const mapDispatchToProps = (dispatch) => {
	return {onClicker: (index) =>{ if (method_delete(index)!=0) {dispatch(deleteMessage(index))} }}
	
}

const mapStateToProps = (state) => {
	let props = {
		messages: state.messages.messages,
	};
	return props;
}

const listPerson = connect(
	mapStateToProps,
    mapDispatchToProps
)(App);

export default listPerson;
