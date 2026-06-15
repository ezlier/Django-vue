<template>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <RouterLink to="/home" class="footer__logo">
          {{ ui.webSetting?.web_name || 'Blog' }}
        </RouterLink>
        <p class="footer__tagline">
          {{ ui.webSetting?.footer_text1 || '记录思考，分享生活' }}
        </p>
      </div>

      <di