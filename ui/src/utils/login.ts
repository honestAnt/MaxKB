export function login() {
  // const login_url = `${import.meta.env.VITE_KEYCLOAK_URL}/realms/${import.meta.env.VITE_KEYCLOAK_REALM}/protocol/openid-connect/auth?client_id=${import.meta.env.VITE_KEYCLOAK_CLIENT}&redirect_uri=${window.location.href}?response_mode=query&response_type=token&scope=openid`
  const url_encode = encodeURIComponent(window.location.href)
  const login_url =  `${import.meta.env.VITE_KEYCLOAK_URL}/login?redirect_uri=${url_encode}`
  window.open(login_url, '_self')
}
