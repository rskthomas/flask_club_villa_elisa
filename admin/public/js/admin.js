function autocompleteMatch(input) {
  if (input == '') {
    return [];
  }
  var reg = new RegExp(input)
  return search_terms.filter(function(term) {
	  if (term.match(reg)) {
  	  return term;
	  }
  });
}

function showResults(val) {
    res = document.getElementById("result");
    res.innerHTML = '';
    if (val == '') {
      return;
    }
    let list = '';
    fetch('/api/members?q=' + val).then(
     function (response) {
       return response.json();
     }).then(function (response) {
        data=response
       for (i=0; i<data.length; i++) {
         list += '<li data-member-id=' + data[i].id + '>' + data[i].personal_id_type + " - " + data[i].personal_id + ' - ' + data[i].last_name + '</li>';
       }
       res.innerHTML = '<ul>' + list + '</ul>';
       return true;
     }).catch(function (err) {
       console.warn('Something went wrong.', err);
       return false;
     });

    res.onclick = function (event) {
        const setValue = event.target.getAttribute('data-member-id');
        document.getElementById("chosen_member_id").value = setValue;
        document.getElementById("member_input").value = event.target.innerText;
        this.innerHTML = "";
    };
}
