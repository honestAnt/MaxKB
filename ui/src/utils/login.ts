export function login() {
  // const login_url = `${import.meta.env.VITE_KEYCLOAK_URL}/realms/${import.meta.env.VITE_KEYCLOAK_REALM}/protocol/openid-connect/auth?client_id=${import.meta.env.VITE_KEYCLOAK_CLIENT}&redirect_uri=${window.location.href}?response_mode=query&response_type=token&scope=openid`
  const login_url = `${import.meta.env.VITE_KEYCLOAK_URL}/login?redirect_uri=${window.location.href}`
  // const login_url = `${import.meta.env.VITE_KEYCLOAK_URL}/login?client_id=${import.meta.env.VITE_KEYCLOAK_CLIENT}&redirect_uri=${window.location.href}&response_mode=query&response_type=token&scope=openid`
  window.open(login_url, '_self')
}
