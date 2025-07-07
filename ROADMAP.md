# 📍 Project Roadmap: Email Agent AI (MVP)

This file tracks planned improvements and known technical debts for future releases of this project.

---

## ✅ Current Status (MVP)

- ✅ Working OAuth 2.0 flow via manual authorization.
- ✅ Gmail API access token and refresh token successfully obtained and saved to `tokens.json`.
- ✅ Manual token refresh script available (`scripts/refresh_tokens.py`).
- ✅ Minimal viable product functionality achieved.

---

## 🚧 Known Improvements (Planned for Future Versions)

### 1. Automatic Token Refreshing
- Currently, access tokens must be manually refreshed via a CLI script.
- Future versions should integrate **automatic token refreshing** into the agent’s runtime.
- This will prevent unexpected token expiry and allow continuous background operation.

### 2. OAuth Flow User Experience Enhancements
- Current OAuth flow requires manual copy-paste of authorization codes from browser redirects.
- Planned future enhancement: auto-detect authorization codes using a temporary local HTTP server.
- This would provide a smoother user experience with fewer manual steps.

### 3. Token Expiration Checks
- Add automatic detection of token expiration before Gmail API calls.
- Trigger refresh automatically when needed.

---

## 💡 Notes
- These improvements are not required for the current MVP.
- They are logged here for future development cycles after core functionality has been validated.

---

_Last updated: July 2025_
