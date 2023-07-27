function saveCheckboxValues() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"][name="tag"]');
    var expires = new Date();
    expires.setDate(expires.getDate() + 7); // 1週間後の日付を設定
  
    checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener('change', valueChange);
  
      if (checkbox.checked) {
        valueChange();
      }
    });
  
    function valueChange() {
      var checkedValues = []; // チェックされた項目の値を保持する配列
  
      checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
          checkedValues.push(checkbox.value); // チェックされた項目の値を配列に追加
        }
      });
  
      var cookieName = "tag_wepon"; // クッキー名
      var cookieValue = checkedValues.join(","); // 配列の値をコンマ区切りで連結
  
      document.cookie = cookieName + "=" + cookieValue + "; expires=" + expires.toUTCString() + "; path=/";
  
      alert("選択された項目の値が保存されました。");
    }
  }
  