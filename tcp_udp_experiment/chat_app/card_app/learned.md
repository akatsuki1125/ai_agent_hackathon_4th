# 学んだことメモ

## カードレイアウトの基本
- カードは div を flex か grid で並べればOK。
- ヘッダーに影響を出さず余白を入れるなら、コンテンツ用のラッパーを作る。

```html
<header class="site-header">My Cards</header>
<div class="content">
  <div class="grid">
    <div class="card">...</div>
  </div>
</div>
```

```css
.content { margin-left: 20px; }
.grid { display: flex; gap: 12px; }
```

## 角丸からヘッダーがはみ出る問題
- 親の角丸からはみ出す場合は overflow を隠すか、角丸を合わせる。

```css
.card { border-radius: 8px; overflow: hidden; }
.card-header { background: #aef; }
```

## ヘッダー内の文字の中央寄せ
- 横方向の中央寄せは text-align か flex でできる。

```css
.card-header { text-align: center; }
```

## 影でカード感を出す
- 薄い影で浮いた感じが出る。

```css
.card { box-shadow: 0 6px 16px rgba(0,0,0,0.12); }
```

## クリックで選択状態の切替
- classList.toggle を使うと簡単にON/OFFできる。

```js
card.addEventListener("click", () => {
  card.classList.toggle("selected");
});
```

```css
.card.selected { transform: scale(1.1); }
```

## 検索バーを中央に配置するヘッダー
- 左/中央/右の3分割で配置が安定する。

```html
<header class="site-header">
  <div class="left">My Cards</div>
  <div class="center"><input class="search" type="search"></div>
  <div class="right"></div>
</header>
```

```css
.site-header { display: flex; align-items: center; }
.left, .center, .right { flex: 1; }
.center { display: flex; justify-content: center; }
```

## 読みやすい筆記体フォント
- Google Fonts の読みやすい筆記体を読み込み、ロゴに適用する。

```html
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap" rel="stylesheet">
```

```css
.logo { font-family: "Dancing Script", cursive; font-weight: 700; }
```
