import React from 'react';


const Person = (props) => (
  <li class="list-group-item">
        <span class="left">
          {props.user.last_name} {props.user.first_name}
        </span> 
        <span class="right">
          {props.user.phone} 
          <button type="submit" class="btn" onClick={()=>{props.onClicker(props.index)}}>
            <i class="icon ion-close-round right"></i>
          </button> 
        </span>  
      </li>  
)

export default Person;

