$(document).ready(function() {
	$("#sidebar li a").click(function(){
		var fn = $(this).attr("fn");
		console.log(fn)
		var url = "/"+fn;

		$.ajax({
		  type: "GET",			// il method
		  url: url,				// la action
		  dataType: "json",
		  data: {
		  },
		  beforeSend: function() {
			  $("#content").html("<img src='images/loader.gif' class='small'>");
		  },
		  success: function(risposta) {
			  if (risposta["status"] == 'OK') {
				  $("#content").html(risposta["html"]);
			  }
			  else {
				  $("#content").html("Errore generico");
			  }
		  },
		  // ed una per il caso di fallimento
		  error: function(){
			  $("#content").html("Errore generico [2]");
		  }
		});
	});
});

function confirmSendEmail(email) {
	if (confirm("Confermi l'invio mail all'indirizzo " + email + " ?")) {
		location = "/sendEmail/"+email;
	}
	else {
		alert("Invio annullato");
	}
	
}
