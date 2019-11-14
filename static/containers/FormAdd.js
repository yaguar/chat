import {connect} from 'react-redux';
import addUser from '../action/adduser';
import React, {Component} from 'react';
import { Field, reduxForm, isInvalid } from 'redux-form';
import validate from '../js/validate';

const renderField = ({ input, label, type, id, meta: { touched, error, invalid} }) => (
  <div class="form-group col-md-4">
    <label for={id}></label>
    <div>
      {label}
      <input {...input} placeholder={label} type={type} id={id} class="form-control" />
      {touched && (error && <div class="nonvalid">{error}</div>)}      
    </div>     
  </div>
)

class FormAdd extends Component {
  render(){
    const { handleSubmit, pristine, reset, submitting } = this.props;
    const submit = (values)=>{this.props.onClicker(values);reset()}
    return (
      <div>	
        <form onSubmit={handleSubmit(submit)}>
          <div class="form-row">
            <Field
            name="first_name"
            id="first_name" 
            component={renderField}
            type="text"
            label="Имя"
            />
            <Field
            name="last_name"
            id="last_name"
            component={renderField}
            type="text"
            label="Фамилия"
            />
            <Field
            name="phone"
            id="phone"
            component={renderField}
            type="tel"
            label="Номер телефона"
            />
           </div>
           <button type="submit" disabled={submitting}  class="btn btn-primary">
            	Добавить
           </button>
         </form>
         <br/>		
       </div>
    )
  }
}

const UsersAdd = reduxForm({
  form: 'FormAdd', // a unique identifier for this form
  validate
})(FormAdd)

function method_post(user){
  fetch('/listcontact', {method:'post',headers: {
     'Accept': 'application/json, text/plain, */*',
     'Content-Type': 'application/json'
    }, body:JSON.stringify({
          first_name: user.first_name,
          last_name: user.last_name,
          phone: user.phone
      })})  
    .then(  
      function(response) {  
        if (response.status != 201){  
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
	return {onClicker: (user) => { if (method_post(user)!=0) {dispatch(addUser(user))}}}
	
}


const mapStateToProps = (state) => {
	let props = {
		users: state.users.users,
	};
	return props;
}

const list = connect(
	mapStateToProps,
	mapDispatchToProps,
)(UsersAdd);

export default list;
