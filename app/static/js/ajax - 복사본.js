$(document).ready(function(){
	$('#login_btn').click(function() {
		$.ajax({
			url:'/login',
			type: 'POST',
			dataType: 'JSON',
			data:{
				id:$('input[name="login_id"]').val()

			},
			success: function(data) {
				if(data.success){
					alert(data.msg);
					console.log(data.msg);
					$('#login').css('display','none');
					$('#chatting').css('display','block');

					pusher = new Pusher('62d7b66cdbddfe53f2fa');
					my_channel = pusher.subscribe('presence-lsy');

					my_channel.bind('pusher:subscription_succeeded', function(members){
						members.each(function(member){
							$('#members').append('<li id = "member_' + member.id +'">' + member.info.username + '</li>');
						})
					})
					my_channel.bind('pusher:member_added', function(member){
						console.log('Member added');
						$('#chat-room').append('<p>' + member.info.username + '님이 입장하셨습니다. </p>');
						$('#members').append('<li id = "member_' + member.id +'">' + member.info.username + '</li>');
						})
					
					my_channel.bind('pusher:member_removed', function(member){
						console.log('Member removed');
						$('#chat-room').append('<p>' + member.info.username + '님이 퇴장하셨습니다. </p>');
						$('#member_' + member.id ).remove();
						})


					my_channel.bind('new_msg', function(data){
						$('#chat-room').append('<p>' +  '<strong>' + data.username +'</strong>' + ' : ' + data.msg + '   ~~ '+ data.time + '</p>');
						$('#chat_msg').val('')
					})
					$('#send').click(function(){
						
						$.ajax({
							url: '/send_msg',
							type: 'POST',
							dataType: 'JSON',
							data: {
								// dNow = new Date();
								// localdate= (dNow.getMonth()+1) + '/' + dNow.getDate() + '/' + dNow.getFullYear() + ' ' + dNow.getHours() + ':' + dNow.getMinutes();
								msg_data: $('#chat_msg').val()
								// name_data: $('#chat_name').val()
								// current_now: localdate
								
							},
							success: function(data) {
								if(data.success){
									console.log('send msg success!');
								}
								else{
									console.log('send msg fail!')
								}

							},
							error : function(data) {
								console.log('Server error!!')
							}	
						})
					})


				}
				else{
					console.log('invalid response!!');

				}
			},

			error: function(resp){
				console.log('No response!!, server error');
			}
		})
})
})