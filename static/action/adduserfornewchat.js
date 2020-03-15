export default function addUserForNewChat(users){
	return{
		type:'USERS_FOR_NEW_CHAT_ADD',
		users
	};
}