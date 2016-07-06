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

    var recipients_amount = 0;

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

    function countMsgs() {
      var msg_len = $("#id_message_text").val().length;
      var msgs = (msg_len > 70) ? Math.ceil(msg_len/67) : 1;
      return { msg_length: msg_len, messages: msgs };
    }

    $("#id_message_text").keyup(function() {
      var msgs = countMsgs();
      $('#characters').text(msgs.msg_length + ' символов (' + msgs.messages + ' сообщений)');
    });

    function getRecipients(pageNumber) {
      var messages_num = countMsgs().messages;
      var limit = 100;
      var offset = (pageNumber-1)*limit;

      var data_dict = [].
      concat(
        $('*[id^="id_regaddress"]').toArray(),
        $('*[id^="id_address"]').toArray(),
        $('*[id^="id_age_"]').toArray(),
        $('*[id="id_family_status"]').toArray(),
        $('*[id="id_education"]').toArray(),
        $('*[id="id_social_category"]').toArray(),
        $('*[id="id_polplace"]').toArray(),
        $('*[id="id_contact"]').toArray(),
        $('*[id="id_candidate"]').toArray(),
        $('*[id^="id_status"]').toArray()
      ).
      map(function(el) {
        return {
          name: el.name,
          val: $(el).is("select") ? +$(el).find(':selected').val() : +$(el).val()
        }
      }).
      filter(function(el) {
        return el.val
      }).
      reduce(function(acc, el) {
        acc[el.name] = el.val
        return acc
      }, {})

      var tbody = $("#recipients-table > tbody:last-child")
      var rec_amount = $('#recipients-amount')
      var camp_cost = $('#campaign-cost')
      var sms_price = $('#sms-price')

      tbody.empty()
      rec_amount.empty()
      camp_cost.empty()
      sms_price.empty()
      tbody.append('Загрузка...')

      $.ajax({
        method: "POST",
        url: "/api/preview_recipients/",
        data: JSON.stringify({"recipients_filter": data_dict, "msg_length": messages_num, "offset": offset, "limit": limit}),
        dataType: "json",
        contentType: "application/json; charset=utf-8"
      }).then(function(data) {
        recipients_amount = data.amount;

        var tbody = $("#recipients-table > tbody:last-child")

        tbody.empty()
        rec_amount.append(data.amount)
        camp_cost.append(data.campaign_cost + " грн")
        sms_price.append(data.sms_price + " грн")
        $(data.recipients).each(function(obj_id, obj) {
          var tr = $('<tr>')
          tbody.append(tr)
          for (attr in data.attrs) {
            var key = data.attrs[attr]
            var ins_val = obj[key] ? obj[key] : '-';
            $(tr).append($('<td>').text(ins_val));
          }
        });
      })
    }


    });
  })(jQuery);
