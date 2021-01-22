$(document).ready(function() {
        $("#loginbutton").click(function(){			// al click del bottone

            $("#msg").html("");

            $.ajax({
              type: "POST",					// il method
              url: "/check",				// la action
              dataType: "json",
              data: {
                  usr:  $("#usr").val(), 	// passaggio parametri via POST
                  pwd:  $("#pwd").val(),
              },
              beforeSend: function() {
                  $("#loginbutton").hide();
                  $("#msg").html("<img src='images/loader.gif' class='small'>");
              },
              // imposto un'azione per il caso di successo, ovvero il server non ha dato errore
              success: function(risposta) {
                  console.log("Ho ricevuto " + risposta);
                  if (risposta["status"] == 'OK') {			// ho scelto che se il login va a buon fine restituisco OK
                        location = '/home';
                  }
                  else {							// altrimenti restituisco KO
                        //alert("Login fallito! Riprova");
                        $("#msg").html("username o password errati");
                        $("#loginbutton").show();
                  }
              },
              // ed una per il caso di fallimento
              error: function(){
                alert("Ooops! Qualcosa e' andato storto...");
                //alert("Login fallito! Riprova");
                $("#loginbutton").show();
                $("#msg").html("");
              }
            });
        });

 });
