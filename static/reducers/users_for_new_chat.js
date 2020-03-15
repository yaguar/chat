let initialState = { users_for_new_chat:[]};
const users_for_new_chat = (state = initialState, action) => {
  switch (action.type) {
    case 'USERS_FOR_NEW_CHAT_ADD':{
      return {users_for_new_chat: [...state.users_for_new_chat, action.users_for_new_chat]}
    };
    case 'USERS_FOR_NEW_CHAT_REMOVE': {
      return {users_for_new_chat: [...state.users_for_new_chat.filter((user, item) =>  item!==action.index)]}
    };
    default:
      return state;
  };
};

export default users_for_new_chat;
