(function($){
  $.fn.extend({
    insertAtCaret: function(myValue){
      return this.each(function(i) {
        if (document.selection) {
          //For browsers like Internet Explorer
          this.focus();
          var sel = document.selection.createRange();
          sel.text = myValue;
          this.focus();
        }
        else if (this.selectionStart || this.selectionStart == '0') {
          //For browsers like Firefox and Webkit based
          var startPos = this.selectionStart;
          var endPos = this.selectionEnd;
          var scrollTop = this.scrollTop;
          this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
          this.focus();
          this.selectionStart = startPos + myValue.length;
          this.selectionEnd = startPos + myValue.length;
          this.scrollTop = scrollTop;
        } else {
          this.value += myValue;
          this.focus();
        }
      });
    }
  });

  $(function(){
    var LASTNAME = ' {lastname}';
    var FIRSTNAME = ' {firstname}';
    var MIDDLENAME = ' {middlename}';
    var CELLPHONE = ' {cellphone}';
    var ADDRESS = ' {address}';

    $('#touch_conditions').hide();
    $('#status_trigger').hide();

    $('#btn-lastname').click(function(){
      $('#id_message_text').insertAtCaret(LASTNAME);
    });

    $('#btn-firstname').click(function(){
      $('#id_message_text').insertAtCaret(FIRSTNAME);
    });

    $('#btn-middlename').click(function(){
      $('#id_message_text').insertAtCaret(MIDDLENAME);
    });

    $('#btn-cellphone').click(function(){
      $('#id_message_text').insertAtCaret(CELLPHONE);
    });

    $('#btn-address').click(function(){
      $('#id_message_text').insertAtCaret(ADDRESS);
    });

    $('#id_to_everyone').change(function(){
      $('#age-filters input').prop('disabled', this.checked);
      $('#address-filters select').prop('disabled', this.checked);
      $('#regaddress-filters select').prop('disabled', this.checked);
    });

    $('#id_triggered_by').change(function(){
      $('#touch_conditions').hide();
      $('#status_trigger').hide();
      var selectedOption = $('#id_triggered_by').find(':selected').val();
      switch (selectedOption) {
        case 'onElectorTouched':
          $('#touch_conditions').show();
          break;
        case 'onElectorStatusChanged':
          $('#status_trigger').show();
          break;
        default:
          $('#touch_conditions').hide();
          $('#status_trigger').hide();
      }
    })

  });
})(jQuery);
