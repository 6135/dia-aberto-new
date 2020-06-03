

var alert = new eliminar();
function eliminar() {
    var operationRef_global = null;
    this.render=function(txt,operationRef = None){
        operationRef_global = operationRef;
        var msg = document.getElementById("msg");
        document.getElementById('text-00').innerHTML = txt;
        document.getElementById('dialog-confirm').style.display = '';
        document.getElementById('dialog-cancel').style.display = '';
        msg.classList.add("is-active");
    }
    this.confirmar=function(){
        if(operationRef_global != null)
            window.location.href = operationRef_global
        else document.getElementById('msg').classList.remove('is-active');
    }
    this.cancelar=function(){
        var msg = document.getElementById("msg");
        document.getElementById('text-00').innerHTML = '';
        operationRef_global = null;
        msg.classList.remove("is-active");
    }
    this.warning=function(txt){
        var msg = document.getElementById('msg');
        document.getElementById('text-00').innerHTML = txt;
        document.getElementById('dialog-confirm').style.display = '';
        document.getElementById('dialog-cancel').style.display = 'none';
        msg.classList.add("is-active");        
    }   
}

function resetForm(){
    oFormObject = document.forms['filter'];
    elements = oFormObject.elements;
    for (var i = 0, element; element = elements[i++];)
        if(element.type != 'hidden')
            element.value='';
}

function displayDetails(idForDetails){
    var objectDetails = document.getElementById("Details"+idForDetails);
    if(objectDetails.style.display == 'none') {
        objectDetails.style.display = "contents";
    } else objectDetails.style.display = "none";

    var x = document.getElementById("mais_informacao"+idForDetails);
    if (x.className === "mdi is-fullwidth mdi-chevron-right mdi-24px") {
      x.className = "mdi is-fullwidth mdi-chevron-down mdi-24px";
    } else {
      x.className = "mdi is-fullwidth mdi-chevron-right mdi-24px";
    }
}

function sortTable(n, isDate) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("table01");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 3); i+=2) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 2].getElementsByTagName("TD")[n];
        
        if(isDate != true) {
            xInner=x.innerHTML.toLowerCase();
            yInner=y.innerHTML.toLowerCase();
        } else {
            xInner=new Date(x.getAttribute('date-value'));
            yInner=new Date(y.getAttribute('date-value'));
        } 
        
        if (dir == "asc") {
            if (xInner > yInner) {
                shouldSwitch = true;
                break;
            }
        } else if (dir == "desc") {
            if (xInner < yInner) {
                shouldSwitch = true;
                break;
            }
        }
    }
    if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 2], rows[i]);
        rows[i].parentNode.insertBefore(rows[i + 3], rows[i+1]);
        switching = true;
        switchcount ++;
    } else {
        if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
      }
    }
  }


  var x = document.getElementById("ordenar");
  if (x.className === "mdi mdi-menu-up") {
    x.className = "mdi mdi-menu-down";
  } else {
    x.className = "mdi mdi-menu-up";
  }

}

function getSchedules(field_id)
{
    var valuedia= $('#'+field_id).val();
    var rowNum = Number(field_id.split('-')[1]);
    console.log(rowNum)
    var number = Number(document.getElementById('id_form-TOTAL_FORMS').value);
    var horarioindisponivel=[]
    for(var i = 0; i < number; i++){
        if(i != rowNum)
            var diaId = "id_form-" + i + "-dia";
            if(document.getElementById(diaId).value == valuedia){
                var horarioId = "id_form-" + i + "-horarioid"
                horarioindisponivel.push(document.getElementById(horarioId).value);
            }
        }
    }
    console.log(horarioindisponivel);
    
    $.ajax({
        url:"/atividades/verhorarios/",
        method: 'POST',
        data: { 
            'horarioindisponivel': JSON.stringify(horarioindisponivel),
            'valuedia': valuedia,
            'id': -1,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            $('#'+field_id).closest('tr').find('.horario-sessao').html(data);
            horarioindisponivel.forEach(function(item,index){
                var stringId = 'id_form-' + field_id.split('-')[1] + '-horarioid ' + 'option[value=\'' + item +'\']';
                $('#'+stringId).remove();
            })
        }

    })

};   

function udpateSchedules(field_id)
{
    var valuedia= $('#'+field_id).val();
    var number = Number(document.getElementById('id_form-TOTAL_FORMS').value);;
    var horarioindisponivel=[]
    for(var i = 0; i < number; i++){
        var diaId = "id_form-" + i + "-dia";
        if(document.getElementById(diaId).value == valuedia){
            var horarioId = "id_form-" + i + "-horarioid"
            horarioindisponivel.push(document.getElementById(horarioId).value);
        }
    }
    console.log(horarioindisponivel);
    
    $.ajax({
        url:"/atividades/verhorarios/",
        method: 'POST',
        data: { 
            'horarioindisponivel': JSON.stringify(horarioindisponivel),
            'valuedia': valuedia,
            'id': -1,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            $('#'+field_id).closest('tr').find('.horario-sessao').html(data);
            horarioindisponivel.forEach(function(item,index){
                var stringId = 'id_form-' + field_id.split('-')[1] + '-horarioid ' + 'option[value=\'' + item +'\']';
                console.log(stringId)
                $('#'+stringId).remove();
            })
        }

    })

};   