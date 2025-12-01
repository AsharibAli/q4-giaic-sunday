const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

interface User {
  id: number;
  username: string;
  email: string;
}

interface Token {
  access_token: string;
  token_type: string;
}

export const register = async (user: Omit<User, 'id'>) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(user),
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  return response.json();
};

export const login = async (user: Omit<User, 'id' | 'username'>) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/login/access-token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(user),
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  const token: Token = await response.json();
  return token;
};
