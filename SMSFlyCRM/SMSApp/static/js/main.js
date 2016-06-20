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

    $('#id_recurrence_weekdays').parent().parent().hide();
    $('#id_recurrence_month_type').parent().parent().hide();

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

    $("input:radio[name=recurrence_type]").click(function() {
      $('#id_recurrence_weekdays').parent().parent().hide();
      $('#id_recurrence_month_type').parent().parent().hide();
      switch ($(this).val()) {
        case 'EVERY_WEEK':
          $('#id_recurrence_weekdays').parent().parent().show();
          break;
        case 'EVERY_MONTH':
          $('#id_recurrence_month_type').parent().parent().show();
          break;
        default:
          $('#id_recurrence_weekdays').parent().parent().hide();
          $('#id_recurrence_month_type').parent().parent().hide();
       }
    });

    $("#id_message_text").keyup(function() {
      var msg_len = $(this).val().length;
      var msgs = (msg_len > 70) ? Math.ceil(msg_len/67) : 1;
      $('#characters').text(msg_len + ' символов (' + msgs + ' сообщений)');
    });

    $("#btn_preview_recipients").click(function() {
      var data_dict = [].
        concat(
          $('*[id^="id_regaddress"]'),
          $('*[id^="id_address"]')
          // $('*[id^="id_age_"]')
        ).
        map(function(el) {
          return {
            name: el.name,
            val: +$(el).find(':selected').val()
          }
        }).
        filter(function(el) {
          return el.val !== '' && el.val !== null
        }).
        reduce(function(acc, el) {
          acc[el.name] = acc[el.val]
          return acc
        }, {})

      var request = $.ajax({
        method: "POST",
        url: "/api/preview_recipients/",
        data: JSON.stringify({"recipients_filter": data_dict}),
        dataType: "json",
        contentType: "application/json; charset=utf-8"
      }).then(function(data) {
        var tr = $('<tr>');
        for (var n = 0; n < data.recipients.length; n++) {
          var el = data.recipients[n];
          for (var prop in el) {
            tr += '<td>' + el[prop] + '</td>';
          }
          tr += '</tr>'
          $("#recipients-table > tbody:last-child").append(tr);
          tr = '<tr>';
        }
      })
    });
  });
})(jQuery);
