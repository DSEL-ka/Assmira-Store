const http = require('node:http');
const https = require('node:https');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const ROOT = __dirname;
loadEnv(path.join(ROOT, '.env'));

const PORT = Number(process.env.PORT || 3000);
const HOST = process.env.HOST || '0.0.0.0';
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '';
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '';
const TRUST_PROXY = process.env.TRUST_PROXY === 'true';
const CATALOG = JSON.parse(fs.readFileSync(path.join(ROOT, 'catalog.json'), 'utf8'));
const PRODUCTS = new Map(CATALOG.products.map((product) => [product.id, product]));
const SIZES = new Set(['XS', 'S', 'M', 'L', 'XL']);
const orderLimits = new Map();

class PublicError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

const server = http.createServer(async (req, res) => {
  setSecurityHeaders(req, res);

  try {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

    if (req.method === 'GET' && url.pathname === '/api/health') {
      return sendJson(res, 200, { ok: true, telegramConfigured: Boolean(TELEGRAM_BOT_TOKEN && TELEGRAM_CHAT_ID) });
    }

    if (req.method === 'POST' && url.pathname === '/api/order') {
      return await handleOrder(req, res);
    }

    if (req.method === 'GET' || req.method === 'HEAD') {
      return serveStatic(req, res, url);
    }

    sendJson(res, 405, { error: 'Метод не поддерживается.' });
  } catch (error) {
    const status = error instanceof PublicError ? error.status : 500;
    const message = error instanceof PublicError ? error.message : 'Внутренняя ошибка сервера.';
    if (!(error instanceof PublicError)) console.error('Server error:', error.message);
    sendJson(res, status, { error: message });
  }
});

server.listen(PORT, () => {
  console.log(`Assmira shop is running on port ${PORT}`);
});server.listen(PORT, HOST, () => {
  console.log(`Assmira shop is running: http://${HOST}:${PORT}`);
  if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
    console.log('Telegram is not configured yet. Copy .env.example to .env and fill TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.');
  }
});

async function handleOrder(req, res) {
  if (!sameOrigin(req)) throw new PublicError(403, 'Запрос отклонён защитой сайта.');
  if (!rateLimit(req, 8, 60_000)) throw new PublicError(429, 'Слишком много заявок. Попробуйте немного позже.');
  if (!String(req.headers['content-type'] || '').includes('application/json')) throw new PublicError(415, 'Неверный формат заявки.');
  if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) throw new PublicError(500, 'Telegram не настроен на сервере.');

  const payload = await readJson(req, 24 * 1024);
  const order = validateOrder(payload);
  await sendTelegram(formatOrder(order));
  sendJson(res, 200, { ok: true, orderId: order.id });
}

function validateOrder(payload) {
  if (!payload || typeof payload !== 'object') throw new PublicError(400, 'Некорректный заказ.');
  if (clean(payload.website, 100)) throw new PublicError(400, 'Заказ отклонён защитой от спама.');

  const customer = payload.customer || {};
  const name = clean(customer.name, 80);
  const phone = clean(customer.phone, 30);
  const email = clean(customer.email, 120);
  const address = clean(customer.address, 220);
  const comment = clean(customer.comment, 600);

  if (name.length < 2) throw new PublicError(400, 'Укажите имя.');
  if (!/^[0-9+()\-\s]{7,30}$/.test(phone)) throw new PublicError(400, 'Укажите корректный телефон.');
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new PublicError(400, 'Укажите корректный email.');
  if (address.length < 5) throw new PublicError(400, 'Укажите адрес доставки.');
  if (!Array.isArray(payload.items) || payload.items.length === 0 || payload.items.length > 30) {
    throw new PublicError(400, 'Корзина пуста или слишком большая.');
  }

  const merged = new Map();
  for (const rawItem of payload.items) {
    const id = Number(rawItem.id);
    const product = PRODUCTS.get(id);
    const size = clean(rawItem.size, 4).toUpperCase();
    const qty = Number(rawItem.qty);
    if (!product || !SIZES.has(size) || !Number.isInteger(qty) || qty < 1 || qty > 20) {
      throw new PublicError(400, 'В заказе есть некорректная позиция.');
    }
    const key = `${id}:${size}`;
    const previous = merged.get(key);
    if (previous) previous.qty += qty;
    else merged.set(key, { id, name: product.name, size, qty, price: product.price });
  }

  const items = [...merged.values()];
  if (items.some((item) => item.qty > 20)) throw new PublicError(400, 'Слишком большое количество одного товара.');
  const total = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  return {
    id: createOrderId(),
    date: new Date().toLocaleString('ru-RU', { timeZone: 'Europe/Moscow' }),
    customer: { name, phone, email, address, comment },
    items,
    total
  };
}

function formatOrder(order) {
  const lines = [
    'Новый заказ Assmira Collection',
    `Номер: ${order.id}`,
    `Дата: ${order.date}`,
    '',
    'Клиент:',
    `Имя: ${order.customer.name}`,
    `Телефон: ${order.customer.phone}`,
    order.customer.email ? `Email: ${order.customer.email}` : null,
    `Адрес: ${order.customer.address}`,
    order.customer.comment ? `Комментарий: ${order.customer.comment}` : null,
    '',
    'Состав заказа:',
    ...order.items.map((item, index) => `${index + 1}. ${item.name}, размер ${item.size}, ${item.qty} шт. x ${formatPrice(item.price)} = ${formatPrice(item.price * item.qty)}`),
    '',
    `Итого: ${formatPrice(order.total)}`
  ];
  return lines.filter(Boolean).join('\n');
}

function sendTelegram(text) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      chat_id: TELEGRAM_CHAT_ID,
      text,
      disable_web_page_preview: true
    });

    const request = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
      method: 'POST',
      timeout: 10_000,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    }, (telegramRes) => {
      let response = '';
      telegramRes.setEncoding('utf8');
      telegramRes.on('data', (chunk) => { response += chunk; });
      telegramRes.on('end', () => {
        if (telegramRes.statusCode >= 200 && telegramRes.statusCode < 300) return resolve();
        console.error('Telegram error:', telegramRes.statusCode, response.slice(0, 300));
        reject(new PublicError(502, 'Telegram временно не принял заказ.'));
      });
    });

    request.on('timeout', () => request.destroy(new PublicError(504, 'Telegram не ответил вовремя.')));
    request.on('error', reject);
    request.end(body);
  });
}

function serveStatic(req, res, url) {
  let filePath;
  if (url.pathname === '/' || url.pathname === '/assmira_final.html') {
    filePath = path.join(ROOT, 'assmira_final.html');
  } else if (url.pathname.startsWith('/img/')) {
    const decodedPath = decodeURIComponent(url.pathname);
    const resolved = path.resolve(ROOT, decodedPath.slice(1));
    const imagesRoot = path.join(ROOT, 'img') + path.sep;
    if (!resolved.startsWith(imagesRoot)) throw new PublicError(403, 'Доступ запрещён.');
    if (!/\.(jpe?g|png|webp)$/i.test(resolved)) throw new PublicError(404, 'Файл не найден.');
    filePath = resolved;
  } else {
    throw new PublicError(404, 'Страница не найдена.');
  }

  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) throw new PublicError(404, 'Файл не найден.');
  res.writeHead(200, { 'Content-Type': contentType(filePath), 'Cache-Control': filePath.endsWith('.html') ? 'no-store' : 'public, max-age=86400' });
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(filePath).pipe(res);
}

function readJson(req, maxBytes) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.setEncoding('utf8');
    req.on('data', (chunk) => {
      body += chunk;
      if (Buffer.byteLength(body) > maxBytes) {
        reject(new PublicError(413, 'Заказ слишком большой.'));
        req.destroy();
      }
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(body || '{}'));
      } catch {
        reject(new PublicError(400, 'Некорректный формат заказа.'));
      }
    });
    req.on('error', reject);
  });
}

function setSecurityHeaders(req, res) {
  res.setHeader('Content-Security-Policy', "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; object-src 'none'");
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=()');
  res.setHeader('Cross-Origin-Resource-Policy', 'same-origin');
  if (req.headers['x-forwarded-proto'] === 'https') {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  }
}

function sameOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return true;
  try {
    return new URL(origin).host === req.headers.host;
  } catch {
    return false;
  }
}

function rateLimit(req, limit, windowMs) {
  const ip = TRUST_PROXY ? String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || req.socket.remoteAddress : req.socket.remoteAddress;
  const key = ip || 'unknown';
  const now = Date.now();
  const bucket = (orderLimits.get(key) || []).filter((time) => now - time < windowMs);
  if (bucket.length >= limit) {
    orderLimits.set(key, bucket);
    return false;
  }
  bucket.push(now);
  orderLimits.set(key, bucket);
  return true;
}

function clean(value, maxLength) {
  return String(value || '')
    .replace(/[\u0000-\u001F\u007F]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maxLength);
}

function sendJson(res, status, payload) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(payload));
}

function contentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.html') return 'text/html; charset=utf-8';
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  if (ext === '.png') return 'image/png';
  if (ext === '.webp') return 'image/webp';
  return 'application/octet-stream';
}

function formatPrice(value) {
  return `${value.toLocaleString('ru-RU')} ₽`;
}

function createOrderId() {
  const date = new Date();
  const stamp = date.toISOString().slice(0, 10).replace(/-/g, '');
  return `AS-${stamp}-${crypto.randomBytes(3).toString('hex').toUpperCase()}`;
}

function loadEnv(envPath) {
  if (!fs.existsSync(envPath)) return;
  const lines = fs.readFileSync(envPath, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim().replace(/^['"]|['"]$/g, '');
    if (key && !process.env[key]) process.env[key] = value;
  }
}
