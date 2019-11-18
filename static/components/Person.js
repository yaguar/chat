import React from 'react';


const Person = (props) => (
  <li class="list-group-item">
        <span class="left">
          {props.message.msg} {props.message.time}
        </span> 
        <span class="right">
          {props.message.user}
          <button type="submit" class="btn" onClick={()=>{props.onClicker(props.index)}}>
            <i class="icon ion-close-round right"></i>
          </button> 
        </span>  
      </li>  
)

export default Person;

