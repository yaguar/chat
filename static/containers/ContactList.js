import {connect} from 'react-redux';
import React, {Component} from 'react';
import deleteUser from '../action/deleteuser';
import Person from '../components/Person';

const App = ({users, onClicker}) => 	(
  <ul class="list-group">
    {users.map((user, index) => (
      <Person key={index} user={user} onClicker={onClicker} index={index}/>  
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
	return {onClicker: (index) =>{ if (method_delete(index)!=0) {dispatch(deleteUser(index))} }}
	
}

const mapStateToProps = (state) => {
	let props = {
		users: state.users.users,
	};
	return props;
}

const listPerson = connect(
	mapStateToProps,
        mapDispatchToProps
)(App);

export default listPerson;
