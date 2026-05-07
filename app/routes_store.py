"""Simple storefront page served by FastAPI."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.core.config import settings

router = APIRouter(tags=["store"])

_STORE_HTML_RAW = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Магазин FastAPI</title>
  <style>
    :root {
      --bg: #0e1320;
      --surface: #141c2f;
      --surface-2: #1a2540;
      --border: #283552;
      --text: #e7eefc;
      --muted: #9caecf;
      --primary: #3b82f6;
      --primary-dark: #2563eb;
      --ok: #34d399;
      --danger: #f87171;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    .container {
      width: min(1200px, 95vw);
      margin: 0 auto;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 2;
      border-bottom: 1px solid var(--border);
      background: rgba(20, 28, 47, 0.95);
      backdrop-filter: blur(6px);
    }
    .topbar {
      background: #111827;
      border-bottom: 1px solid #24304a;
    }
    .topbar-row {
      display: grid;
      grid-template-columns: 170px 1fr auto;
      gap: 0.8rem;
      align-items: center;
      padding: 0.7rem 0;
    }
    .topbar-row-2 {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      align-items: center;
      padding: 0 0 0.7rem 0;
    }
    .topbar-row-2 input {
      flex: 1 1 260px;
      min-width: 220px;
    }
    .topbar-row-2 button {
      flex: 0 0 auto;
      white-space: nowrap;
    }
    .brand {
      font-size: 1.4rem;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: 0.2px;
    }
    .search-wrap input {
      width: 100%;
      border-radius: 8px;
      border: 1px solid #4b5563;
      background: #f8fafc;
      color: #111827;
      padding: 0.62rem 0.8rem;
    }
    .top-controls {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .top-controls .ghost {
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 36px;
    }
    .top-controls .cart-top-btn {
      display: none;
      text-decoration: none;
      min-height: 36px;
    }
    .top-controls .account-btn {
      display: none;
      min-height: 36px;
    }
    .header-inner {
      padding: 1rem 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }
    h1 { margin: 0; font-size: 1.2rem; }
    .muted { color: var(--muted); font-size: 0.92rem; }
    a { color: #93c5fd; }
    main { padding: 1.2rem 0 2rem; }
    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 1rem;
    }
    .panel {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--surface);
      padding: 1rem;
    }
    .filters {
      display: grid;
      grid-template-columns: 1.3fr 1fr 1fr auto;
      gap: 0.6rem;
      margin-bottom: 1rem;
    }
    input, select, button {
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--border);
      color: var(--text);
      background: var(--surface-2);
      padding: 0.55rem 0.7rem;
      font: inherit;
    }
    button {
      cursor: pointer;
      width: auto;
    }
    button.primary {
      background: var(--primary);
      border-color: var(--primary-dark);
      color: #fff;
      font-weight: 600;
    }
    button.primary:hover { filter: brightness(1.08); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 0.8rem;
    }
    .product {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.85rem;
      background: var(--surface-2);
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      min-height: 220px;
    }
    .product h3 {
      margin: 0;
      font-size: 1rem;
      line-height: 1.25;
    }
    .price { color: var(--ok); font-weight: 700; }
    .stock { color: var(--muted); font-size: 0.88rem; }
    .cart h2 {
      margin: 0 0 0.75rem;
      font-size: 1.05rem;
    }
    .cart-line {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 0.45rem;
      border-bottom: 1px solid var(--border);
      padding: 0.55rem 0;
    }
    .qty-controls {
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      margin-top: 0.2rem;
    }
    .qty-controls button {
      width: 28px;
      height: 28px;
      padding: 0;
    }
    .checkout {
      display: grid;
      gap: 0.5rem;
      margin-top: 1rem;
    }
    .auth-tabs {
      display: flex;
      gap: 0.6rem;
      margin-bottom: 0.4rem;
    }
    .auth-tab {
      width: 50%;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      padding: 0.6rem 0.6rem;
      cursor: pointer;
      font: inherit;
    }
    button.auth-tab.primary {
      background: var(--primary);
      border-color: var(--primary-dark);
      color: #fff;
      font-weight: 600;
    }
    .auth-panel {
      display: block;
      margin-bottom: 0.2rem;
    }
    .msg {
      margin-top: 0.7rem;
      padding: 0.65rem 0.75rem;
      border-radius: 8px;
      background: #113427;
      color: #99f6c8;
      border: 1px solid #14532d;
      display: none;
    }
    .msg.err {
      background: #3a1c1c;
      color: #fecaca;
      border-color: #7f1d1d;
    }
    .summary { font-size: 0.92rem; color: var(--muted); }
    .p-img {
      width: 100%;
      height: 150px;
      border-radius: 10px;
      object-fit: cover;
      border: 1px solid rgba(255, 255, 255, 0.06);
      background: rgba(255, 255, 255, 0.03);
    }
    .product .meta-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .rating {
      display: inline-flex;
      gap: 2px;
      align-items: center;
      color: #ffd166;
      font-weight: 700;
      font-size: 0.92rem;
    }
    .rating .stars {
      letter-spacing: 1px;
      font-size: 1rem;
    }
    .rating .count {
      color: var(--muted);
      font-weight: 500;
      font-size: 0.85rem;
    }
    .p-open {
      cursor: pointer;
    }
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.65);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.2rem;
      z-index: 10;
    }
    .modal {
      width: min(980px, 98vw);
      max-height: 88vh;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(20, 28, 47, 0.98);
      backdrop-filter: blur(6px);
      box-shadow: 0 18px 60px rgba(0,0,0,0.55);
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      padding: 1rem 1.1rem 0.5rem;
      border-bottom: 1px solid var(--border);
    }
    .modal-header h2 {
      margin: 0;
      font-size: 1.15rem;
    }
    .ghost {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.5rem 0.7rem;
      cursor: pointer;
      width: auto;
    }
    .ghost:hover {
      border-color: rgba(255,255,255,0.18);
    }
    .modal-body {
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 1rem;
      padding: 1rem 1.1rem 1.2rem;
    }
    .modal-body .left {
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }
    .modal-body .right {
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }
    .reviews {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.8rem;
      background: rgba(255,255,255,0.02);
      display: grid;
      gap: 0.75rem;
    }
    .review {
      border-bottom: 1px dashed rgba(255,255,255,0.12);
      padding-bottom: 0.6rem;
    }
    .review:last-child { border-bottom: none; padding-bottom: 0; }
    .review .who {
      color: var(--muted);
      font-size: 0.88rem;
    }
    .review .comment {
      margin-top: 0.25rem;
      white-space: pre-wrap;
    }
    textarea {
      width: 100%;
      min-height: 90px;
      resize: vertical;
    }
    .star-select {
      display: flex;
      gap: 0.4rem;
      align-items: center;
      flex-wrap: wrap;
    }
    .star-select select {
      width: auto;
      min-width: 90px;
    }
    @media (max-width: 860px) {
      .modal-body { grid-template-columns: 1fr; }
    }
    @media (max-width: 980px) {
      .layout { grid-template-columns: 1fr; }
      .filters { grid-template-columns: 1fr 1fr; }
      .topbar-row {
        grid-template-columns: 1fr;
      }
      .topbar-row-2 {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="container topbar-row">
      <div class="brand" id="storeTitle">FastAPI Store</div>
      <div class="search-wrap">
        <input id="searchInput" placeholder="Search products..." />
      </div>
      <div class="top-controls">
        <button id="langToggleBtn" class="ghost" type="button">EN</button>
        <a id="registerPageLink" class="ghost" href="/register">Реєстрація</a>
        <button id="accountBtn" class="ghost account-btn" type="button">Акаунт</button>
        <button id="cartTopBtn" class="ghost cart-top-btn" type="button">Кошик (0)</button>
        <span id="cartQuickCount" class="muted">0</span>
      </div>
    </div>
    <div class="container topbar-row-2">
      <input type="email" id="email" placeholder="Email" autocomplete="username" />
      <input type="password" id="password" placeholder="Пароль" autocomplete="current-password" />
      <button class="primary" id="loginBtn" type="button">Увійти</button>
      <button id="logoutBtn" type="button">Вийти</button>
    </div>
  </header>

  <main class="container">
    <section class="panel">
      <div class="filters">
        <select id="catFilter"><option value="">Усі категорії</option></select>
        <select id="sortSelect">
          <option value="name-asc">Назва A-Я</option>
          <option value="price-asc">Ціна: від меншої</option>
          <option value="price-desc">Ціна: від більшої</option>
          <option value="stock-desc">Наявність: більше</option>
        </select>
        <button class="primary" id="reloadBtn" type="button">Оновити</button>
      </div>
      <div id="products" class="grid"></div>
      <div id="msg" class="msg"></div>
    </section>
  </main>

  <div id="checkoutBackdrop" class="modal-backdrop">
    <div class="modal" style="width:min(760px,98vw);" role="dialog" aria-modal="true">
      <div class="modal-header">
        <h2 id="checkoutTitle">Оформлення замовлення</h2>
        <button id="checkoutCloseBtn" class="ghost" type="button">Закрити</button>
      </div>
      <div class="modal-body" style="grid-template-columns:1fr; gap:0.8rem;">
        <div id="checkoutCartLines"></div>
        <div id="checkoutSummary" class="summary">Кошик порожній.</div>
        <div class="panel" style="padding:0.9rem;background:rgba(255,255,255,0.02);">
          <div id="checkoutDetailsTitle" style="font-weight:700; margin-bottom:0.6rem;">Дані доставки</div>
          <input id="checkoutName" type="text" placeholder="Ім'я та прізвище" />
          <input id="checkoutPhone" type="text" placeholder="Телефон" />
          <input id="checkoutAddress" type="text" placeholder="Адреса доставки" />
          <textarea id="checkoutNote" placeholder="Коментар до замовлення (необов'язково)"></textarea>
        </div>
        <div class="checkout">
          <button class="primary" id="checkoutBtn" type="button">Оформити замовлення</button>
          <button id="clearBtn" type="button">Очистити кошик</button>
        </div>
      </div>
    </div>
  </div>

  <div id="addBackdrop" class="modal-backdrop">
    <div class="modal" style="width:min(520px,98vw);" role="dialog" aria-modal="true">
      <div class="modal-header">
        <h2 id="addTitle">Додати в кошик</h2>
        <button id="addCloseBtn" class="ghost" type="button">Закрити</button>
      </div>
      <div class="modal-body" style="grid-template-columns:1fr; gap:0.8rem;">
        <div class="panel" style="padding:0.9rem;background:rgba(255,255,255,0.02);">
          <div id="addProductName" style="font-weight:800; font-size:1.05rem;"></div>
          <div id="addProductPrice" class="price" style="margin-top:0.35rem;"></div>
          <div class="muted" id="addProductStock" style="margin-top:0.25rem;"></div>
          <div style="display:flex; gap:0.6rem; align-items:center; margin-top:0.8rem;">
            <span class="muted" id="addQtyLabel">Кількість</span>
            <input id="addQty" type="number" min="1" value="1" style="width:120px;" />
          </div>
        </div>
        <div class="checkout">
          <button class="primary" id="addConfirmBtn" type="button">Додати</button>
          <button id="addCancelBtn" type="button">Скасувати</button>
        </div>
      </div>
    </div>
  </div>

  <div id="accountBackdrop" class="modal-backdrop">
    <div class="modal" style="width:min(520px,98vw);" role="dialog" aria-modal="true">
      <div class="modal-header">
        <h2 id="accountTitle">Керування акаунтом</h2>
        <button id="accountCloseBtn" class="ghost" type="button">Закрити</button>
      </div>
      <div class="modal-body" style="grid-template-columns:1fr; gap:0.8rem;">
        <div class="panel" style="padding:0.9rem;background:rgba(255,255,255,0.02);">
          <div class="muted" id="accountEmail"></div>
          <div style="font-weight:800; margin-top:0.8rem;" id="nicknameTitle">Нікнейм</div>
          <input id="nicknameInput" type="text" placeholder="Ваш нік" />
          <button class="primary" id="saveNicknameBtn" type="button">Зберегти нік</button>
          <div style="font-weight:800; margin-top:0.8rem;" id="changePassTitle">Зміна пароля</div>
          <input id="currentPass" type="password" placeholder="Поточний пароль" autocomplete="current-password" />
          <input id="newPass" type="password" placeholder="Новий пароль" autocomplete="new-password" />
          <input id="newPass2" type="password" placeholder="Повторіть новий пароль" autocomplete="new-password" />
          <button class="primary" id="changePassBtn" type="button">Змінити пароль</button>
          <div id="accountMsg" class="msg" style="display:none;"></div>
        </div>
        <div class="checkout">
          <button id="logoutFromAccountBtn" type="button">Вийти з акаунта</button>
        </div>
      </div>
    </div>
  </div>

  <div id="modalBackdrop" class="modal-backdrop">
    <div id="modal" class="modal" role="dialog" aria-modal="true">
      <div class="modal-header">
        <h2 id="modalTitle">Товар</h2>
        <button id="modalClose" class="ghost" type="button">Закрити</button>
      </div>
      <div class="modal-body">
        <div class="left">
          <img id="modalImage" class="p-img" alt="Зображення товару" />
          <div class="rating" id="modalRating">
            <span class="stars">★★★★★</span>
            <span class="count">0 відгуків</span>
          </div>
        </div>
        <div class="right">
          <div class="muted" id="modalCategory"></div>
          <div class="price" id="modalPrice"></div>
          <div class="stock" id="modalStock"></div>

          <div class="reviews">
            <div id="modalReviews"></div>
          </div>

          <div class="panel" style="padding:0.9rem;background:rgba(255,255,255,0.02);border-radius:12px;">
            <div id="reviewHeading" style="font-weight:700;margin-bottom:0.5rem;">Написати відгук</div>
            <div class="star-select">
              <label id="reviewRatingLabel" style="min-width:90px;">Оцінка</label>
              <select id="reviewRating">
                <option value="5">5 - Відмінно</option>
                <option value="4">4</option>
                <option value="3">3</option>
                <option value="2">2</option>
                <option value="1">1 - Погано</option>
              </select>
            </div>
            <textarea id="reviewComment" placeholder="Поділіться враженнями..."></textarea>
            <div style="display:flex;gap:0.6rem;align-items:center;margin-top:0.6rem;">
              <button class="primary" id="reviewSubmit" type="button">Надіслати відгук</button>
              <div id="reviewMsg" class="muted" style="margin-left:auto;"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const API = "__API_V1__";
    const CART_KEY = "bas_store_cart";
    const REVIEW_KEY = "bas_store_reviews";
    const LANG_KEY = "bas_store_lang";
    const USD_TO_UAH = 40;
    let lang = localStorage.getItem(LANG_KEY) || "uk";
    let products = [];
    let categories = [];
    let currentUser = null;
    let activeProductId = null;

    const STR = {
      uk: {
        langToggle: "EN",
        storeTitle: "Магазин FastAPI",
        storeSubtitle: "Демо вітрина товарів, кошик, авторизація та оформлення замовлення",
        tabLogin: "Увійти",
        tabRegister: "Реєстрація",
        searchPlaceholder: "Пошук товарів...",
        allCategories: "Усі категорії",
        sortNameAsc: "Назва A-Я",
        sortPriceAsc: "Ціна: від меншої",
        sortPriceDesc: "Ціна: від більшої",
        sortStockDesc: "Наявність: більше",
        refresh: "Оновити",

        cartEmpty: "Кошик порожній.",
        emailPlaceholder: "Email",
        passwordPlaceholder: "Пароль",
        loginBtn: "Увійти",
        logoutBtn: "Вийти",

        registerEmailPlaceholder: "Email для реєстрації",
        registerPasswordPlaceholder: "Новий пароль",
        registerPassword2Placeholder: "Повторіть пароль",
        registerBtn: "Створити акаунт",

        checkoutBtn: "Оформити замовлення",
        clearBtn: "Очистити кошик",
        cartButtonTop: "Кошик",
        accountButtonTop: "Акаунт",
        checkoutTitle: "Оформлення замовлення",
        checkoutDetailsTitle: "Дані доставки",
        checkoutName: "Ім'я та прізвище",
        checkoutPhone: "Телефон",
        checkoutAddress: "Адреса доставки",
        checkoutNote: "Коментар до замовлення (необов'язково)",

        loginFailed: "Вхід не вдався. Спробуйте buyer@example.com / buyerpass.",
        loginSuccess: "Ви увійшли. Можете оформити замовлення.",
        logoutSuccess: "Ви вийшли.",

        enterRegistrationEmail: "Введіть email для реєстрації.",
        passwordMin: "Пароль має бути мінімум 6 символів.",
        passwordsMismatch: "Паролі не збігаються.",
        registrationFailed: "Не вдалося зареєструватися",
        accountCreated: "Акаунт створено. Виконуємо вхід...",

        itemsLabel: "шт.",
        totalLabel: "сума",
        catalogUnavailable: "Каталог недоступний. Перевірте контейнер API.",

        cartEmptyCheckout: "Кошик порожній.",
        loginFirstCheckout: "Спочатку увійдіть.",
        orderFailed: "Не вдалося оформити замовлення",
        orderSuccess: "Замовлення №{id} оформлено. Сума {total}.",

        uncategorized: "Без категорії",
        noDescription: "Немає опису",
        inStockPrefix: "В наявності",
        addToCart: "Додати в кошик",
        reviewsSuffix: "відгуків",
        anonymous: "анонім",
        cartCleared: "Кошик очищено.",

        modalProduct: "Товар",
        close: "Закрити",
        productImageAlt: "Зображення товару",
        reviewsNoReviews: "Поки немає відгуків. Будьте першим!",

        reviewHeading: "Написати відгук",
        ratingLabel: "Оцінка",
        reviewCommentPlaceholder: "Поділіться враженнями...",
        reviewSubmit: "Надіслати відгук",

        loginToReview: "Увійдіть, щоб залишити відгук.",
        openProductToReview: "Відкрийте товар, щоб залишити відгук.",
        chooseRating: "Оберіть оцінку від 1 до 5.",
        longerCommentMin: "Напишіть довший коментар (мінімум 3 символи).",
        reviewThankYou: "Дякуємо! Відгук надіслано.",
        addToCartTitle: "Додати в кошик",
        addQty: "Кількість",
        addConfirm: "Додати",
        addCancel: "Скасувати",
        accountTitle: "Керування акаунтом",
        changePasswordTitle: "Зміна пароля",
        currentPassword: "Поточний пароль",
        newPassword: "Новий пароль",
        repeatNewPassword: "Повторіть новий пароль",
        changePasswordBtn: "Змінити пароль",
        logoutAccountBtn: "Вийти з акаунта",
        nicknameTitle: "Нікнейм",
        nicknamePlaceholder: "Ваш нік",
        saveNicknameBtn: "Зберегти нік",
        nicknameSaved: "Нік оновлено.",
        nicknameTaken: "Такий нік вже зайнятий.",
        fillPasswords: "Заповніть усі поля пароля.",
        passwordsNoMatch: "Паролі не збігаються.",
        passwordChanged: "Пароль змінено.",
      },
      en: {
        langToggle: "UA",
        storeTitle: "FastAPI Store",
        storeSubtitle: "Demo product listing, cart, auth and checkout",
        tabLogin: "Log in",
        tabRegister: "Register",
        searchPlaceholder: "Search products...",
        allCategories: "All categories",
        sortNameAsc: "Name A-Z",
        sortPriceAsc: "Price low-high",
        sortPriceDesc: "Price high-low",
        sortStockDesc: "Stock high-low",
        refresh: "Refresh",

        cartEmpty: "Cart is empty.",
        emailPlaceholder: "Email",
        passwordPlaceholder: "Password",
        loginBtn: "Log in",
        logoutBtn: "Log out",

        registerEmailPlaceholder: "Registration email",
        registerPasswordPlaceholder: "New password",
        registerPassword2Placeholder: "Repeat password",
        registerBtn: "Create account",

        checkoutBtn: "Place order",
        clearBtn: "Clear cart",
        cartButtonTop: "Cart",
        accountButtonTop: "Account",
        checkoutTitle: "Checkout",
        checkoutDetailsTitle: "Shipping details",
        checkoutName: "Full name",
        checkoutPhone: "Phone",
        checkoutAddress: "Shipping address",
        checkoutNote: "Order note (optional)",

        loginFailed: "Login failed. Try buyer@example.com / buyerpass.",
        loginSuccess: "You are logged in. You can place an order.",
        logoutSuccess: "You are logged out.",

        enterRegistrationEmail: "Enter registration email.",
        passwordMin: "Password must be at least 6 characters.",
        passwordsMismatch: "Passwords do not match.",
        registrationFailed: "Registration failed",
        accountCreated: "Account created. Logging you in...",

        itemsLabel: "items",
        totalLabel: "total",
        catalogUnavailable: "Catalog is unavailable. Check API container.",

        cartEmptyCheckout: "Cart is empty.",
        loginFirstCheckout: "Please log in first.",
        orderFailed: "Order failed",
        orderSuccess: "Order #{id} created. Total {total}.",

        uncategorized: "Uncategorized",
        noDescription: "No description",
        inStockPrefix: "In stock",
        addToCart: "Add to cart",
        reviewsSuffix: "reviews",
        anonymous: "anonymous",
        cartCleared: "Cart cleared.",

        modalProduct: "Product",
        close: "Close",
        productImageAlt: "Product image",
        reviewsNoReviews: "No reviews yet. Be the first!",

        reviewHeading: "Write a review",
        ratingLabel: "Rating",
        reviewCommentPlaceholder: "Share your experience...",
        reviewSubmit: "Submit review",

        loginToReview: "Log in to write a review.",
        openProductToReview: "Open a product to review.",
        chooseRating: "Choose rating from 1 to 5.",
        longerCommentMin: "Write a longer comment (min 3 chars).",
        reviewThankYou: "Thank you! Review submitted.",
        addToCartTitle: "Add to cart",
        addQty: "Quantity",
        addConfirm: "Add",
        addCancel: "Cancel",
        accountTitle: "Account settings",
        changePasswordTitle: "Change password",
        currentPassword: "Current password",
        newPassword: "New password",
        repeatNewPassword: "Repeat new password",
        changePasswordBtn: "Change password",
        logoutAccountBtn: "Log out",
        nicknameTitle: "Nickname",
        nicknamePlaceholder: "Your nickname",
        saveNicknameBtn: "Save nickname",
        nicknameSaved: "Nickname updated.",
        nicknameTaken: "Nickname already taken.",
        fillPasswords: "Fill all password fields.",
        passwordsNoMatch: "Passwords do not match.",
        passwordChanged: "Password changed.",
      },
    };

    function t(key) {
      return STR[lang][key];
    }

    function loadReviews() {
      try {
        return JSON.parse(localStorage.getItem(REVIEW_KEY) || "{}");
      } catch {
        return {};
      }
    }

    function saveReviews(reviewsByProduct) {
      localStorage.setItem(REVIEW_KEY, JSON.stringify(reviewsByProduct));
    }

    function getProductReviews(productId) {
      const reviewsByProduct = loadReviews();
      return Array.isArray(reviewsByProduct[String(productId)]) ? reviewsByProduct[String(productId)] : [];
    }

    function upsertProductReviews(productId, newReviews) {
      const reviewsByProduct = loadReviews();
      reviewsByProduct[String(productId)] = newReviews;
      saveReviews(reviewsByProduct);
    }

    function starsText(rating) {
      const val = Number(rating);
      const filled = Math.max(0, Math.min(5, Math.round(val)));
      return "★".repeat(filled) + "☆".repeat(5 - filled);
    }

    function productImage(p) {
      // Inline SVG to avoid external image hosting.
      const seed = Number(p.id) || 1;
      const hue = (seed * 47) % 360;
      const name = (p.name || "").trim();
      const short = name.length > 18 ? name.slice(0, 18) + "…" : name;
      const svg =
        `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">` +
        `<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">` +
        `<stop offset="0" stop-color="hsl(${hue},90%,55%)" />` +
        `<stop offset="1" stop-color="hsl(${(hue + 40) % 360},90%,45%)" />` +
        `</linearGradient></defs>` +
        `<rect width="600" height="600" rx="36" fill="url(#g)"/>` +
        `<circle cx="480" cy="140" r="90" fill="rgba(255,255,255,0.14)"/>` +
        `<text x="40" y="320" font-family="Arial, sans-serif" font-size="42" fill="rgba(255,255,255,0.92)" font-weight="700">${short.replace(
          /&/g,
          "&amp;"
        )}</text>` +
        `<text x="40" y="392" font-family="Arial, sans-serif" font-size="22" fill="rgba(255,255,255,0.86)">${"Зображення (демо)"}</text>` +
        `</svg>`;
      return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
    }

    async function fetchMe() {
      try {
        const r = await fetch(`${API}/auth/me`, { credentials: "include" });
        if (!r.ok) {
          currentUser = null;
          return null;
        }
        currentUser = await r.json();
        return currentUser;
      } catch {
        currentUser = null;
        return null;
      }
    }

    function closeModal() {
      activeProductId = null;
      const b = document.getElementById("modalBackdrop");
      b.style.display = "none";
    }

    function renderModalReviews(productId) {
      const holder = document.getElementById("modalReviews");
      const reviews = getProductReviews(productId).slice().sort((a, b) => (b.createdAt || "").localeCompare(a.createdAt || ""));

      if (!reviews.length) {
        holder.innerHTML = `<div class="muted">${t("reviewsNoReviews")}</div>`;
        return;
      }

      holder.innerHTML = "";
      for (const rev of reviews) {
        const when = rev.createdAt ? new Date(rev.createdAt).toLocaleString() : "";
        const el = document.createElement("div");
        el.className = "review";
        const stars = starsText(rev.rating);
        el.innerHTML =
          `<div class="rating"><span class="stars">${stars}</span><span class="count">${rev.rating}/5</span></div>` +
          `<div class="who">${escapeHtml(rev.userDisplay || rev.userEmail || t("anonymous"))} • ${escapeHtml(when)}</div>` +
          `<div class="comment">${escapeHtml(rev.comment || "")}</div>`;
        holder.appendChild(el);
      }
    }

    async function openProductModal(productId) {
      activeProductId = productId;
      const p = products.find((x) => x.id === productId);
      if (!p) return;

      document.getElementById("modalTitle").textContent = p.name;
      document.getElementById("modalImage").src = productImage(p);
      document.getElementById("modalCategory").textContent =
        categories.find((c) => c.id === p.category_id)?.name || t("uncategorized");
      document.getElementById("modalPrice").textContent = formatMoney(p.price);
      document.getElementById("modalStock").textContent = `${t("inStockPrefix")}: ${p.stock}`;

      const reviews = getProductReviews(productId);
      const avg = reviews.length ? reviews.reduce((a, r) => a + Number(r.rating || 0), 0) / reviews.length : 0;
      const avgText = reviews.length ? avg.toFixed(1) : "0.0";
      document.getElementById("modalRating").innerHTML =
        `<span class="stars">${starsText(avg)}</span><span class="count">${avgText} • ${reviews.length} ${t("reviewsSuffix")}</span>`;

      document.getElementById("reviewRating").value = "5";
      document.getElementById("reviewComment").value = "";
      document.getElementById("reviewMsg").textContent = "";
      renderModalReviews(productId);

      document.getElementById("modalBackdrop").style.display = "flex";
      const user = await fetchMe();
      const reviewMsg = document.getElementById("reviewMsg");
      reviewMsg.textContent = user ? "" : t("loginToReview");
    }

    async function submitReview() {
      const productId = activeProductId;
      if (!productId) {
        setMsg(t("openProductToReview"), true);
        return;
      }
      const rating = Number(document.getElementById("reviewRating").value);
      const comment = document.getElementById("reviewComment").value.trim();

      if (!rating || rating < 1 || rating > 5) {
        document.getElementById("reviewMsg").textContent = t("chooseRating");
        return;
      }
      if (!comment || comment.length < 3) {
        document.getElementById("reviewMsg").textContent = t("longerCommentMin");
        return;
      }

      const user = currentUser || (await fetchMe());
      if (!user) {
        document.getElementById("reviewMsg").textContent = t("loginToReview");
        return;
      }

      const reviews = getProductReviews(productId);
      const display = (user.nickname && String(user.nickname).trim()) ? String(user.nickname).trim() : user.email;
      reviews.push({
        id: Date.now(),
        userEmail: user.email,
        userDisplay: display,
        rating,
        comment,
        createdAt: new Date().toISOString(),
      });

      upsertProductReviews(productId, reviews);
      renderModalReviews(productId);
      renderProducts();

      document.getElementById("reviewComment").value = "";
      document.getElementById("reviewMsg").textContent = t("reviewThankYou");
    }

    function escapeHtml(value) {
      const e = document.createElement("div");
      e.textContent = value ?? "";
      return e.innerHTML;
    }

    function money(value) {
      const n = Number(value);
      return (Number.isFinite(n) ? n : 0).toFixed(2);
    }

    function formatMoney(usdValue) {
      const n = Number(usdValue);
      const base = Number.isFinite(n) ? n : 0;
      const converted = lang === "uk" ? base * USD_TO_UAH : base;
      const symbol = lang === "uk" ? "₴" : "$";
      return `${symbol}${money(converted)}`;
    }

    function applyLang() {
      document.documentElement.lang = lang === "uk" ? "uk" : "en";
      document.getElementById("langToggleBtn").textContent = t("langToggle");

      // Header
      document.getElementById("storeTitle").textContent = t("storeTitle");
      const subtitle = document.getElementById("storeSubtitle");
      if (subtitle) subtitle.textContent = t("storeSubtitle");

      // Filters
      document.getElementById("searchInput").placeholder = t("searchPlaceholder");
      const catFilter = document.getElementById("catFilter");
      if (catFilter && catFilter.options.length > 0) catFilter.options[0].textContent = t("allCategories");

      const sortSelect = document.getElementById("sortSelect");
      if (sortSelect) {
        for (const opt of sortSelect.options) {
          if (opt.value === "name-asc") opt.textContent = t("sortNameAsc");
          if (opt.value === "price-asc") opt.textContent = t("sortPriceAsc");
          if (opt.value === "price-desc") opt.textContent = t("sortPriceDesc");
          if (opt.value === "stock-desc") opt.textContent = t("sortStockDesc");
        }
      }
      document.getElementById("reloadBtn").textContent = t("refresh");

      // Cart summary is set by renderCart() / renderProducts().

      document.getElementById("registerPageLink").textContent = t("tabRegister");
      document.getElementById("cartTopBtn").textContent = `${t("cartButtonTop")} (${document.getElementById("cartQuickCount").textContent || "0"})`;
      document.getElementById("accountBtn").textContent = t("accountButtonTop");

      document.getElementById("email").placeholder = t("emailPlaceholder");
      document.getElementById("password").placeholder = t("passwordPlaceholder");
      document.getElementById("loginBtn").textContent = t("loginBtn");
      document.getElementById("logoutBtn").textContent = t("logoutBtn");

      document.getElementById("checkoutBtn").textContent = t("checkoutBtn");
      document.getElementById("clearBtn").textContent = t("clearBtn");
      document.getElementById("checkoutTitle").textContent = t("checkoutTitle");
      document.getElementById("checkoutDetailsTitle").textContent = t("checkoutDetailsTitle");
      document.getElementById("checkoutName").placeholder = t("checkoutName");
      document.getElementById("checkoutPhone").placeholder = t("checkoutPhone");
      document.getElementById("checkoutAddress").placeholder = t("checkoutAddress");
      document.getElementById("checkoutNote").placeholder = t("checkoutNote");
      document.getElementById("checkoutCloseBtn").textContent = t("close");

      document.getElementById("addTitle").textContent = t("addToCartTitle");
      document.getElementById("addCloseBtn").textContent = t("close");
      document.getElementById("addQtyLabel").textContent = t("addQty");
      document.getElementById("addConfirmBtn").textContent = t("addConfirm");
      document.getElementById("addCancelBtn").textContent = t("addCancel");

      document.getElementById("accountTitle").textContent = t("accountTitle");
      document.getElementById("accountCloseBtn").textContent = t("close");
      document.getElementById("nicknameTitle").textContent = t("nicknameTitle");
      document.getElementById("nicknameInput").placeholder = t("nicknamePlaceholder");
      document.getElementById("saveNicknameBtn").textContent = t("saveNicknameBtn");
      document.getElementById("changePassTitle").textContent = t("changePasswordTitle");
      document.getElementById("currentPass").placeholder = t("currentPassword");
      document.getElementById("newPass").placeholder = t("newPassword");
      document.getElementById("newPass2").placeholder = t("repeatNewPassword");
      document.getElementById("changePassBtn").textContent = t("changePasswordBtn");
      document.getElementById("logoutFromAccountBtn").textContent = t("logoutAccountBtn");

      // Modal static parts
      document.getElementById("modalTitle").textContent = t("modalProduct");
      document.getElementById("modalClose").textContent = t("close");
      document.getElementById("modalImage").alt = t("productImageAlt");
      // Update review heading + label by querying first matching nodes (simple/robust)
      const heading = document.querySelector('[id="reviewHeading"]');
      if (heading) heading.textContent = t("reviewHeading");
      const ratingLabel = document.querySelector('[id="reviewRatingLabel"]');
      if (ratingLabel) ratingLabel.textContent = t("ratingLabel");

      document.getElementById("reviewComment").placeholder = t("reviewCommentPlaceholder");
      document.getElementById("reviewSubmit").textContent = t("reviewSubmit");

      const reviewRatingSelect = document.getElementById("reviewRating");
      if (reviewRatingSelect) {
        for (const opt of reviewRatingSelect.options) {
          if (opt.value === "5") opt.textContent = lang === "uk" ? "5 - Відмінно" : "5 - Excellent";
          if (opt.value === "4") opt.textContent = "4";
          if (opt.value === "3") opt.textContent = "3";
          if (opt.value === "2") opt.textContent = "2";
          if (opt.value === "1") opt.textContent = lang === "uk" ? "1 - Погано" : "1 - Bad";
        }
      }

      if (activeProductId) {
        openProductModal(activeProductId);
      }
    }

    function updateAuthUI() {
      const authRow = document.querySelector(".topbar-row-2");
      const registerLink = document.getElementById("registerPageLink");
      const cartBtn = document.getElementById("cartTopBtn");
      const accountBtn = document.getElementById("accountBtn");
      const loggedIn = Boolean(currentUser);
      if (authRow) authRow.style.display = loggedIn ? "none" : "grid";
      if (registerLink) registerLink.style.display = loggedIn ? "none" : "inline-flex";
      if (cartBtn) cartBtn.style.display = loggedIn ? "inline-flex" : "none";
      if (accountBtn) accountBtn.style.display = loggedIn ? "inline-flex" : "none";
    }

    function openAddModal(product) {
      document.getElementById("addProductName").textContent = product.name;
      document.getElementById("addProductPrice").textContent = formatMoney(product.price);
      document.getElementById("addProductStock").textContent = `${t("inStockPrefix")}: ${product.stock}`;
      const qty = document.getElementById("addQty");
      qty.value = "1";
      qty.max = String(Math.max(1, product.stock));
      document.getElementById("addConfirmBtn").dataset.pid = String(product.id);
      document.getElementById("addBackdrop").style.display = "flex";
    }

    function closeAddModal() {
      document.getElementById("addBackdrop").style.display = "none";
    }

    function openAccountModal() {
      document.getElementById("accountEmail").textContent = currentUser ? currentUser.email : "";
      document.getElementById("nicknameInput").value = currentUser && currentUser.nickname ? String(currentUser.nickname) : "";
      const msg = document.getElementById("accountMsg");
      msg.style.display = "none";
      msg.textContent = "";
      document.getElementById("currentPass").value = "";
      document.getElementById("newPass").value = "";
      document.getElementById("newPass2").value = "";
      document.getElementById("accountBackdrop").style.display = "flex";
    }

    function closeAccountModal() {
      document.getElementById("accountBackdrop").style.display = "none";
    }

    async function changePassword() {
      const cur = document.getElementById("currentPass").value;
      const n1 = document.getElementById("newPass").value;
      const n2 = document.getElementById("newPass2").value;
      const box = document.getElementById("accountMsg");

      function show(text, err=false) {
        box.style.display = "block";
        box.textContent = text;
        box.className = "msg" + (err ? " err" : "");
      }

      if (!cur || !n1 || !n2) {
        show(t("fillPasswords"), true);
        return;
      }
      if (n1 !== n2) {
        show(t("passwordsNoMatch"), true);
        return;
      }

      const resp = await fetch(`${API}/auth/change-password`, {
        method: "POST",
        credentials: "include",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ current_password: cur, new_password: n1 }),
      });
      if (!resp.ok) {
        const d = await resp.json().catch(() => ({}));
        show(d.detail ? String(d.detail) : "Error", true);
        return;
      }
      show(t("passwordChanged"));
    }

    async function saveNickname() {
      const nickname = document.getElementById("nicknameInput").value.trim();
      const box = document.getElementById("accountMsg");
      function show(text, err=false) {
        box.style.display = "block";
        box.textContent = text;
        box.className = "msg" + (err ? " err" : "");
      }
      if (nickname.length < 2) {
        show(t("nicknamePlaceholder"), true);
        return;
      }
      const resp = await fetch(`${API}/auth/set-nickname`, {
        method: "POST",
        credentials: "include",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ nickname }),
      });
      if (!resp.ok) {
        const d = await resp.json().catch(() => ({}));
        const msg = d.detail ? String(d.detail) : t("nicknameTaken");
        show(msg, true);
        return;
      }
      await fetchMe();
      show(t("nicknameSaved"));
    }

    function loadCart() {
      try {
        return JSON.parse(localStorage.getItem(CART_KEY) || "[]");
      } catch {
        return [];
      }
    }

    function saveCart(cart) {
      localStorage.setItem(CART_KEY, JSON.stringify(cart));
    }

    function setMsg(text, isErr = false) {
      const box = document.getElementById("msg");
      if (!text) {
        box.style.display = "none";
        box.textContent = "";
        box.className = "msg";
        return;
      }
      box.style.display = "block";
      box.textContent = text;
      box.className = "msg" + (isErr ? " err" : "");
    }

    function upsertCart(product, delta) {
      const cart = loadCart();
      const idx = cart.findIndex((x) => x.id === product.id);
      if (idx >= 0) {
        cart[idx].qty += delta;
        if (cart[idx].qty <= 0) cart.splice(idx, 1);
      } else if (delta > 0) {
        cart.push({
          id: product.id,
          name: product.name,
          price: Number(product.price),
          qty: delta,
        });
      }
      saveCart(cart);
      renderCart();
    }

    function changeQty(productId, delta) {
      const item = products.find((p) => p.id === productId);
      if (!item) return;
      upsertCart(item, delta);
    }

    function renderCart() {
      const cart = loadCart();
      const holder = document.getElementById("checkoutCartLines");
      holder.innerHTML = "";
      let totalQty = 0;
      let totalPrice = 0;

      for (const line of cart) {
        totalQty += line.qty;
        totalPrice += Number(line.price) * Number(line.qty);
        const row = document.createElement("div");
        row.className = "cart-line";
        row.innerHTML =
          `<div>` +
            `<div>${escapeHtml(line.name)}</div>` +
            `<div class="qty-controls">` +
              `<button type="button" data-minus="${line.id}">-</button>` +
              `<span>${line.qty}</span>` +
              `<button type="button" data-plus="${line.id}">+</button>` +
            `</div>` +
          `</div>` +
          `<strong>${formatMoney(line.price * line.qty)}</strong>`;
        holder.appendChild(row);
      }

      holder.querySelectorAll("[data-minus]").forEach((b) => {
        b.addEventListener("click", () => changeQty(Number(b.dataset.minus), -1));
      });
      holder.querySelectorAll("[data-plus]").forEach((b) => {
        b.addEventListener("click", () => changeQty(Number(b.dataset.plus), 1));
      });

      document.getElementById("checkoutSummary").textContent =
        totalQty > 0 ? `${totalQty} ${t("itemsLabel")}, ${t("totalLabel")}: ${formatMoney(totalPrice)}` : t("cartEmpty");
      const quick = document.getElementById("cartQuickCount");
      if (quick) quick.textContent = `${totalQty}`;
      const cartBtn = document.getElementById("cartTopBtn");
      if (cartBtn) cartBtn.textContent = `${t("cartButtonTop")} (${totalQty})`;
    }

    function filteredProducts() {
      const search = document.getElementById("searchInput").value.trim().toLowerCase();
      const catValue = document.getElementById("catFilter").value;
      const sort = document.getElementById("sortSelect").value;
      const catId = catValue ? Number(catValue) : null;

      let out = products.filter((p) => {
        const searchHit = !search
          || p.name.toLowerCase().includes(search)
          || (p.description || "").toLowerCase().includes(search);
        const catHit = catId == null || p.category_id === catId;
        return searchHit && catHit;
      });

      if (sort === "price-asc") out.sort((a, b) => Number(a.price) - Number(b.price));
      else if (sort === "price-desc") out.sort((a, b) => Number(b.price) - Number(a.price));
      else if (sort === "stock-desc") out.sort((a, b) => Number(b.stock) - Number(a.stock));
      else out.sort((a, b) => a.name.localeCompare(b.name));

      return out;
    }

    function renderProducts() {
      const root = document.getElementById("products");
      root.innerHTML = "";

      const list = filteredProducts();
      for (const p of list) {
        const rawCategory = categories.find((c) => c.id === p.category_id)?.name || t("uncategorized");
        const category = lang === "uk"
          ? ({ "Electronics": "Електроніка", "Books": "Книги" }[rawCategory] || rawCategory)
          : ({ "Електроніка": "Electronics", "Книги": "Books" }[rawCategory] || rawCategory);
        const imgSrc = productImage(p);
        const reviews = getProductReviews(p.id);
        const avg = reviews.length ? reviews.reduce((a, r) => a + Number(r.rating || 0), 0) / reviews.length : 0;
        const avgText = reviews.length ? avg.toFixed(1) : "0.0";
        const ratingStars = starsText(avg);
        const card = document.createElement("article");
        card.className = "product";
        card.classList.add("p-open");
        card.dataset.open = String(p.id);
        card.innerHTML =
          `<img class="p-img" src="${imgSrc}" alt="${escapeHtml(p.name)}" />` +
          `<div class="meta-row">` +
            `<h3>${escapeHtml(p.name)}</h3>` +
            `<div class="rating">` +
              `<span class="stars">${ratingStars}</span>` +
              `<span class="count">${avgText} • ${reviews.length} ${t("reviewsSuffix")}</span>` +
            `</div>` +
          `</div>` +
          `<div class="muted">${escapeHtml(category)}</div>` +
          `<div>${escapeHtml(p.description || t("noDescription"))}</div>` +
          `<div class="price">${formatMoney(p.price)}</div>` +
          `<div class="stock">${t("inStockPrefix")}: ${p.stock}</div>` +
          `<div>` +
            `<button type="button" class="primary" data-add="${p.id}" ${p.stock < 1 ? "disabled" : ""}>${t("addToCart")}</button>` +
          `</div>`;
        root.appendChild(card);
      }

      root.querySelectorAll("[data-open]").forEach((card) => {
        card.addEventListener("click", () => openProductModal(Number(card.dataset.open)));
      });

      root.querySelectorAll("[data-add]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const id = Number(btn.dataset.add);
          const product = products.find((x) => x.id === id);
          if (product) openAddModal(product);
        });
      });
    }

    async function refreshData() {
      setMsg("");
      const [catResp, prodResp] = await Promise.all([
        fetch(`${API}/categories`, { credentials: "include" }),
        fetch(`${API}/products`, { credentials: "include" }),
      ]);
      categories = await catResp.json();
      products = await prodResp.json();

      const cat = document.getElementById("catFilter");
      while (cat.options.length > 1) cat.remove(1);
      for (const c of categories) {
        const option = document.createElement("option");
        option.value = String(c.id);
        option.textContent = c.name;
        cat.appendChild(option);
      }
      renderProducts();
    }

    async function login() {
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
      const resp = await fetch(`${API}/auth/login`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!resp.ok) {
        setMsg(t("loginFailed"), true);
        return;
      }
      await fetchMe();
      updateAuthUI();
      setMsg(t("loginSuccess"));
    }

    async function logout() {
      await fetch(`${API}/auth/logout`, { method: "POST", credentials: "include" });
      currentUser = null;
      updateAuthUI();
      closeCheckoutModal();
      setMsg(t("logoutSuccess"));
    }

    function openCheckoutModal() {
      document.getElementById("checkoutBackdrop").style.display = "flex";
      renderCart();
    }

    function closeCheckoutModal() {
      document.getElementById("checkoutBackdrop").style.display = "none";
    }

    async function checkout() {
      const cart = loadCart();
      if (!cart.length) {
        setMsg(t("cartEmptyCheckout"), true);
        return;
      }

      // Lightweight checkout details validation for more detailed flow.
      const fullName = document.getElementById("checkoutName").value.trim();
      const phone = document.getElementById("checkoutPhone").value.trim();
      const address = document.getElementById("checkoutAddress").value.trim();
      if (!fullName || !phone || !address) {
        setMsg(lang === "uk" ? "Заповніть ім'я, телефон та адресу доставки." : "Fill full name, phone, and shipping address.", true);
        return;
      }

      const items = cart.map((x) => ({ product_id: x.id, quantity: x.qty }));
      const resp = await fetch(`${API}/orders`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "pending", items }),
      });
      if (resp.status === 401) {
        setMsg(t("loginFirstCheckout"), true);
        return;
      }
      if (!resp.ok) {
        const detail = await resp.json().catch(() => ({}));
        setMsg(detail.detail ? JSON.stringify(detail.detail) : t("orderFailed"), true);
        return;
      }
      const order = await resp.json();
      saveCart([]);
      renderCart();
      await refreshData();
      const msg = t("orderSuccess")
        .replace("{id}", order.id)
        .replace("{total}", formatMoney(order.total_amount));
      setMsg(msg);
      closeCheckoutModal();
    }

    document.getElementById("searchInput").addEventListener("input", renderProducts);
    document.getElementById("catFilter").addEventListener("change", renderProducts);
    document.getElementById("sortSelect").addEventListener("change", renderProducts);
    document.getElementById("reloadBtn").addEventListener("click", refreshData);
    document.getElementById("loginBtn").addEventListener("click", login);
    document.getElementById("logoutBtn").addEventListener("click", logout);
    document.getElementById("cartTopBtn").addEventListener("click", openCheckoutModal);
    document.getElementById("checkoutBtn").addEventListener("click", checkout);
    document.getElementById("checkoutCloseBtn").addEventListener("click", closeCheckoutModal);
    document.getElementById("checkoutBackdrop").addEventListener("click", (e) => {
      if (e.target && e.target.id === "checkoutBackdrop") closeCheckoutModal();
    });
    document.getElementById("addCloseBtn").addEventListener("click", closeAddModal);
    document.getElementById("addCancelBtn").addEventListener("click", closeAddModal);
    document.getElementById("addBackdrop").addEventListener("click", (e) => {
      if (e.target && e.target.id === "addBackdrop") closeAddModal();
    });
    document.getElementById("addConfirmBtn").addEventListener("click", () => {
      const pid = Number(document.getElementById("addConfirmBtn").dataset.pid || "0");
      const qty = Number(document.getElementById("addQty").value || "1");
      const product = products.find((x) => x.id === pid);
      if (!product) return;
      const q = Math.max(1, Math.min(qty, Number(product.stock || 1)));
      upsertCart(product, q);
      closeAddModal();
    });

    document.getElementById("accountBtn").addEventListener("click", openAccountModal);
    document.getElementById("accountCloseBtn").addEventListener("click", closeAccountModal);
    document.getElementById("accountBackdrop").addEventListener("click", (e) => {
      if (e.target && e.target.id === "accountBackdrop") closeAccountModal();
    });
    document.getElementById("changePassBtn").addEventListener("click", changePassword);
    document.getElementById("saveNicknameBtn").addEventListener("click", saveNickname);
    document.getElementById("logoutFromAccountBtn").addEventListener("click", async () => {
      await logout();
      closeAccountModal();
    });
    document.getElementById("clearBtn").addEventListener("click", () => {
      saveCart([]);
      renderCart();
      setMsg(t("cartCleared"));
    });

    document.getElementById("modalClose").addEventListener("click", closeModal);
    document.getElementById("modalBackdrop").addEventListener("click", (e) => {
      if (e.target && e.target.id === "modalBackdrop") closeModal();
    });
    document.getElementById("reviewSubmit").addEventListener("click", submitReview);
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeModal();
        closeCheckoutModal();
        closeAddModal();
        closeAccountModal();
      }
    });

    document.getElementById("langToggleBtn").addEventListener("click", () => {
      lang = lang === "uk" ? "en" : "uk";
      localStorage.setItem(LANG_KEY, lang);
      applyLang();
      renderProducts();
      renderCart();
    });

    applyLang();

    fetchMe().then(() => updateAuthUI());
    refreshData().catch(() => setMsg(t("catalogUnavailable"), true));
    renderCart();
  </script>
</body>
</html>
"""

_STORE_HTML = _STORE_HTML_RAW.replace("__API_V1__", settings.API_V1_STR)

_REGISTER_HTML_RAW = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Реєстрація</title>
  <style>
    body { margin: 0; font-family: "Segoe UI", system-ui, sans-serif; background: #0f172a; color: #e2e8f0; }
    .wrap { min-height: 100vh; display: grid; place-items: center; padding: 1rem; }
    .card { width: min(460px, 96vw); background: #111c34; border: 1px solid #29406a; border-radius: 14px; padding: 1.2rem; }
    h1 { margin: 0 0 0.35rem; font-size: 1.4rem; }
    p { margin: 0 0 1rem; color: #9fb1ce; }
    input, button, a {
      width: 100%; border-radius: 10px; border: 1px solid #2a3f68; padding: 0.68rem 0.8rem; margin-bottom: 0.6rem;
      font: inherit; box-sizing: border-box;
    }
    input { background: #1a2747; color: #e5edff; }
    button { background: #3b82f6; color: #fff; font-weight: 700; cursor: pointer; }
    .ghost { background: transparent; color: #c7d2fe; text-decoration: none; text-align: center; display: inline-block; }
    .row { display: grid; grid-template-columns: 1fr auto; gap: 0.6rem; align-items: center; margin-bottom: 0.6rem; }
    .msg { display: none; border-radius: 10px; padding: 0.7rem 0.8rem; margin-top: 0.2rem; border: 1px solid #365a9a; background: #13294d; }
    .msg.err { border-color: #7f1d1d; background: #3a1d1d; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="row">
        <h1 id="title">Реєстрація</h1>
        <button id="langBtn" type="button" style="width:auto;padding:0.5rem 0.7rem;margin:0;">EN</button>
      </div>
      <p id="subtitle">Створіть акаунт і поверніться в магазин.</p>
      <input id="email" type="email" placeholder="Email для реєстрації" autocomplete="email" />
      <input id="nickname" type="text" placeholder="Нікнейм" autocomplete="nickname" />
      <input id="password" type="password" placeholder="Новий пароль" autocomplete="new-password" />
      <input id="password2" type="password" placeholder="Повторіть пароль" autocomplete="new-password" />
      <button id="submitBtn" type="button">Створити акаунт</button>
      <a id="backLink" href="/store" class="ghost">Назад у магазин</a>
      <div id="msg" class="msg"></div>
    </div>
  </div>
  <script>
    const API = "__API_V1__";
    const LANG_KEY = "bas_store_lang";
    let lang = localStorage.getItem(LANG_KEY) || "uk";
    const STR = {
      uk: {
        title: "Реєстрація",
        subtitle: "Створіть акаунт і поверніться в магазин.",
        email: "Email для реєстрації",
        nick: "Нікнейм",
        p1: "Новий пароль",
        p2: "Повторіть пароль",
        submit: "Створити акаунт",
        back: "Назад у магазин",
        needEmail: "Введіть email.",
        needNick: "Введіть нікнейм (мін. 2 символи).",
        shortPass: "Пароль має бути мінімум 6 символів.",
        mismatch: "Паролі не збігаються.",
        fail: "Не вдалося зареєструватися",
        ok: "Акаунт створено! Повертаємо в магазин...",
        lang: "EN",
      },
      en: {
        title: "Register",
        subtitle: "Create account and return to store.",
        email: "Registration email",
        nick: "Nickname",
        p1: "New password",
        p2: "Repeat password",
        submit: "Create account",
        back: "Back to store",
        needEmail: "Enter email.",
        needNick: "Enter nickname (min 2 chars).",
        shortPass: "Password must be at least 6 characters.",
        mismatch: "Passwords do not match.",
        fail: "Registration failed",
        ok: "Account created! Returning to store...",
        lang: "UA",
      }
    };
    function t(k){ return STR[lang][k]; }
    function applyLang(){
      document.documentElement.lang = lang === "uk" ? "uk" : "en";
      document.getElementById("title").textContent = t("title");
      document.getElementById("subtitle").textContent = t("subtitle");
      document.getElementById("email").placeholder = t("email");
      document.getElementById("nickname").placeholder = t("nick");
      document.getElementById("password").placeholder = t("p1");
      document.getElementById("password2").placeholder = t("p2");
      document.getElementById("submitBtn").textContent = t("submit");
      document.getElementById("backLink").textContent = t("back");
      document.getElementById("langBtn").textContent = t("lang");
    }
    function showMsg(text, err=false){
      const m = document.getElementById("msg");
      m.style.display = "block";
      m.className = "msg" + (err ? " err" : "");
      m.textContent = text;
    }
    async function submit(){
      const email = document.getElementById("email").value.trim();
      const nickname = document.getElementById("nickname").value.trim();
      const password = document.getElementById("password").value;
      const password2 = document.getElementById("password2").value;
      if(!email){ showMsg(t("needEmail"), true); return; }
      if(!nickname || nickname.length < 2){ showMsg(t("needNick"), true); return; }
      if(!password || password.length < 6){ showMsg(t("shortPass"), true); return; }
      if(password !== password2){ showMsg(t("mismatch"), true); return; }
      const resp = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({email, password, nickname}),
      });
      if(!resp.ok){
        const d = await resp.json().catch(()=>({}));
        showMsg(d.detail ? (typeof d.detail === "string" ? d.detail : JSON.stringify(d.detail)) : t("fail"), true);
        return;
      }
      showMsg(t("ok"));
      setTimeout(() => { window.location.href = "/store"; }, 900);
    }
    document.getElementById("submitBtn").addEventListener("click", submit);
    document.getElementById("langBtn").addEventListener("click", () => {
      lang = lang === "uk" ? "en" : "uk";
      localStorage.setItem(LANG_KEY, lang);
      applyLang();
    });
    applyLang();
  </script>
</body>
</html>
"""

_REGISTER_HTML = _REGISTER_HTML_RAW.replace("__API_V1__", settings.API_V1_STR)


@router.get("/store", response_class=HTMLResponse, include_in_schema=False)
async def store_page() -> HTMLResponse:
    return HTMLResponse(content=_STORE_HTML)


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_page() -> HTMLResponse:
    return HTMLResponse(content=_REGISTER_HTML)
