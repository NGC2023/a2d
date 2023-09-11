// PIN input move cursor

function moveToNext(currentInput, nextInputName) {
    if (currentInput.value.length >= currentInput.maxLength) {
        const nextInput = document.getElementsByName(nextInputName)[0];
        nextInput.focus();
    }
}

//Advanced config checkbox requirement

function validateForm() {
    var checkboxes = document.getElementsByName('ssids[]');
    var checked = false;
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        checked = true;
        break;
      }
    }
    if (!checked) {
      alert('Select at least one SSID or -0 for no SSID.');
      return false;
    }
    return true;
  }
