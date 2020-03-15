export default function rewriteDialogs(users){
	return{
		type:'REWRITE_MAYBE_USERS_FOR_NEW_CHAT',
		users
	};
}