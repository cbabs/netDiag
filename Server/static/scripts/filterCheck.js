
	
	var regxTen = /tn-(.*?)(\/)/ //Ten regex
	var regxCntrct = /brc-(.*)(\/)/  //Contract regex
	var regxSubj = /subj-(.*)/  //Subj regex 
	
	
		$(function() {
		  $('a#process_input').bind('click', function() {
			$.getJSON('/_api/getfilters', {
			  filter: $('input[name="filter"]').val(),
			}, function(data) {
			  $("#numOfsubjcts").text(data.result.cntrctsUsingFltrs + " subjects using this filter:");
			  var filtersData = data.result.contrcts;
			  console.log(data);
			  //$("#subjects").text(filtersData.each());
			  var id = document.querySelector("#subjects");
			  while(id.firstChild){
				  id.removeChild(id.firstChild);
			  }
			  filtersData.forEach((cntr)=>{
				  
				  //console.log(cntr)
				  var tenMatch = regxTen.exec(cntr)
				  var cntrctMatch = regxCntrct.exec(cntr)
				  var subjMatch = regxSubj.exec(cntr)
				  
				  var prettyCntr = ("Tenant: " + tenMatch[1] + " > Contract: " +
						  cntrctMatch[1] + " > Subject: " + subjMatch[1]);
				  //console.log(prettyCntr);
				  var newList = document.createElement('li')
				  newList.innerHTML = prettyCntr
				  id.appendChild(newList)
				  
			  })
			  
			});
			return false;
		  });
		});
