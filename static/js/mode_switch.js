document.addEventListener("DOMContentLoaded", function() {
  const checkbox = document.getElementById("switch");
  // 以下のコードをここに移動してください


const title = document.querySelector('.title');

// ページロード時にクッキーからスイッチの状態を読み取る
const switchState = getCookie('switchState');
if (switchState === 'on') {
  checkbox.checked = true;
  title.textContent = '個別検索モード';
} else {
  checkbox.checked = false;
  title.textContent = 'ノーマルモード';
}

// クッキーにスイッチの状態を保存する関数
function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + value + "; " + expires + "; path=/";
}

// クッキーから値を取得する関数
function getCookie(name) {
  const cookieName = name + "=";
  const cookieArray = document.cookie.split(';');
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) === ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return "";
}

// スイッチの状態が変わったらクッキーに保存する
checkbox.addEventListener('click', () => {
  if (checkbox.checked) {
    title.textContent = '個別検索モード';
    setCookie('switchState', 'on', 30); // 30日間有効なクッキーとして保存
  } else {
    title.textContent = 'ノーマルモード';
    setCookie('switchState', 'off', 30); // 30日間有効なクッキーとして保存
  }
});

});