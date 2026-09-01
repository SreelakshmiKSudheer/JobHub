/**
 * JWT Decoder helper utility.
 */

export interface DecodedToken {
  sub: string; // User ID
  role: 'admin' | 'user';
  version?: number;
  exp?: number;
  token_type?: string;
}

export const decodeJwt = (token: string): DecodedToken | null => {
  try {
    const base64Url = token.split('.')[1];
    if (!base64Url) return null;

    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => `%${(`00${c.charCodeAt(0).toString(16)}`).slice(-2)}`)
        .join('')
    );

    return JSON.parse(jsonPayload) as DecodedToken;
  } catch (error) {
    console.error('Failed to decode JWT token:', error);
    return null;
  }
};

export const isTokenExpired = (token: string): boolean => {
  const decoded = decodeJwt(token);
  if (!decoded || !decoded.exp) return true;
  const currentTime = Math.floor(Date.now() / 1000);
  return decoded.exp < currentTime;
};
