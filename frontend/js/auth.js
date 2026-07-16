// Firebase auth helper (module)
// Usage: create js/firebase-config.js (copy firebase-config.example.js)

import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js';
import {
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  setPersistence,
  browserLocalPersistence,
  onAuthStateChanged,
  signOut
} from 'https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js';

(function(){
  if(!window.FIREBASE_CONFIG){
    console.warn('FIREBASE_CONFIG not found. Copy js/firebase-config.example.js -> js/firebase-config.js and fill values. Auth will be disabled until configured.');
    // create a stub so UI doesn't break
    window.openLoginModal = function(){ alert('Auth not configured. See js/firebase-config.example.js'); };
    window.logout = function(){};
    return;
  }

  const app = initializeApp(window.FIREBASE_CONFIG);
  const auth = getAuth(app);

  // Use local persistence so user stays signed in across refreshes
  setPersistence(auth, browserLocalPersistence).catch(()=>{});

  const provider = new GoogleAuthProvider();

  window.openLoginModal = async function(){
    try{
      await signInWithPopup(auth, provider);
    }catch(err){
      console.error('Login failed', err);
      alert('Login failed: '+ (err.message||err));
    }
  };

  window.logout = async function(){
    try{ await signOut(auth); }
    catch(err){ console.error('Logout failed', err); }
  };

  function renderUser(user){
    const userArea = document.getElementById('userArea');
    if(!userArea) return;
    if(user){
      const name = user.displayName || user.email.split('@')[0];
      const photo = user.photoURL || '';
      userArea.innerHTML = `
        <div style="display:flex;align-items:center;gap:8px">
          <img src="${photo}" alt="${name}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.12)">
          <span style="color:white;font-weight:700">${name}</span>
          <button class="btn btn-ghost" onclick="logout()">Logout</button>
        </div>
      `;
    } else {
      userArea.innerHTML = `<button class="btn btn-primary" id="loginBtn" onclick="openLoginModal()">👤 Login</button>`;
    }
  }

  // Expose a helper to require auth on protected pages
  window.requireAuth = function(redirectTo){
    const redirect = redirectTo||'/index.html';
    if(getAuth().currentUser){ return Promise.resolve(getAuth().currentUser); }
    return new Promise((resolve)=>{
      const unsub = onAuthStateChanged(auth, (user)=>{
        unsub();
        if(!user){ window.location.href = redirect; }
        else resolve(user);
      });
    });
  };

  // Watch auth state
  onAuthStateChanged(auth, (user)=>{
    renderUser(user);

    // If body has data-protected="true" and user is null, redirect to index
    if(document.body && document.body.dataset && document.body.dataset.protected === 'true'){
      if(!user){ setTimeout(()=>{ window.location.href = '/index.html'; }, 600);
      }
    }
  });

  // Helpers for other scripts to call
  window.getCurrentUser = function(){ return auth.currentUser; };

  window.getIdToken = async function(forceRefresh=false){
    const user = auth.currentUser;
    if(!user) return null;
    try{ return await user.getIdToken(forceRefresh); }
    catch(e){ console.error('getIdToken failed', e); return null; }
  };

  window.getAuthHeader = async function(){
    const token = await window.getIdToken();
    const headers = { 'Content-Type': 'application/json' };
    if(token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  };

})();
