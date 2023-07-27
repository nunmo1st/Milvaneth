document.addEventListener('DOMContentLoaded', function() {
  saveCheckboxValues();
});

function saveCheckboxValues() {
  var checkboxes = document.querySelectorAll('input[type="checkbox"][name="item_tag"]');
  var expires = new Date();
  expires.setDate(expires.getDate() + 7); // 1週間後の日付を設定

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', valueChange);
  });

  function valueChange() {
    var checkedValues = []; // チェックされた項目の値を保持する配列

    checkboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        checkedValues.push(checkbox.value); // チェックされた項目の値を配列に追加
      }
    });

    var cookieName = "tag_wepon"; // クッキー名
    var existingValues = getCookieValues(); // クッキーに保存されている値を取得

    // 重複を除いた配列を作成
    var filteredValues = existingValues.filter(function(value) {
      return !checkedValues.includes(value);
    });
    filteredValues.push(...checkedValues);

    var cookieValue = filteredValues.join(","); // 重複を除いた値をコンマ区切りで連結

    document.cookie = cookieName + "=" + cookieValue + "; expires=" + expires.toUTCString() + "; path=/";

    alert("選択された項目の値が保存されました。");
  }

  // クッキーから値を取得してチェックボックスに反映する処理を追加
  var existingValues = getCookieValues();
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = existingValues.includes(checkbox.value.toString());
  });
}

function getCookieValues() {
  var cookieName = 'tag_wepon'; // クッキー名
  var cookieValue = document.cookie
    .split(';')
    .map(function(cookie) {
      return cookie.trim();
    })
    .find(function(cookie) {
      return cookie.startsWith(cookieName + '=');
    });

  if (cookieValue) {
    // クッキー値から値部分のみを抽出して返す
    return cookieValue.split('=')[1].split(',');
  }

  return []; // クッキーが存在しない場合は空の配列を返す
}

function getAllCheckboxValues() {
  var checkboxes = document.querySelectorAll('input[type="checkbox"][name="item_tag"]');
  var allValues = [];
  checkboxes.forEach(function(checkbox) {
    allValues.push(checkbox.value);
  });
  return allValues;
}

var checkboxValues = getAllCheckboxValues();
console.log(checkboxValues);
