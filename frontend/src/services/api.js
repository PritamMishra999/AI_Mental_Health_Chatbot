const BASE_URL = 'http://localhost:8000';

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  console.log(`API Request: ${options.method || 'GET'} ${url}`);
  if (options.body) {
    console.log(`Request Body:`, JSON.parse(options.body));
  }
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    });

    let data;
    try {
      data = await response.json();
    } catch (e) {
      data = { detail: `HTTP ${response.status}: ${response.statusText}` };
    }

    console.log(`API Response: ${response.status}`, data);

    if (!response.ok) {
      const errorMsg = data?.detail || data?.message || JSON.stringify(data) || `HTTP ${response.status}`;
      console.error(`API Error Details:`, { status: response.status, error: data, fullResponse: data });
      throw new Error(errorMsg);
    }

    return data;
  } catch (err) {
    console.error('API Error:', err);
    throw err;
  }
}

export async function register(email, password, fullName) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email: email.trim(),
      password: password.trim(),
      full_name: fullName.trim(),
    }),
  });
}

export async function login(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email: email.trim(),
      password: password.trim(),
    }),
  });
}

export async function sendMessage(message, token) {
  return request('/chat/message', {
    method: 'POST',
    body: JSON.stringify({ message: message.trim() }),
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
}

