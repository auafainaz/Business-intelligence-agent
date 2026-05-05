# ClientIQ Frontend

Next.js frontend for the ClientIQ inbound realtime voice intelligence MVP.

## Local Run

Start the frontend in a new PowerShell terminal:

```powershell
cd frontend
npm run dev
```

Open:

```text
http://127.0.0.1:3000
```

Dashboard route example:

```text
http://127.0.0.1:3000/dashboard/virtusa-2
```

## If `npm` Is Not Recognized

If Node.js is installed through the portable local setup, run:

```powershell
$nodeRoot = "$env:LOCALAPPDATA\Programs\NodePortable\node-v22.22.2-win-x64"
$env:Path = "$nodeRoot;$env:Path"
npm run dev
```

If Node.js is not installed yet, install Node.js LTS from:

```text
https://nodejs.org/
```

Then close and reopen PowerShell and check:

```powershell
node --version
npm --version
```

## Build Check

Run this before pushing changes:

```powershell
cd "C:\Users\aboof\OneDrive - N-able (Pvt) Ltd\ABOO\Work\Projects\Business intelligence agent\frontend"
npm run build
```

If using portable Node:

```powershell
$nodeRoot = "$env:LOCALAPPDATA\Programs\NodePortable\node-v22.22.2-win-x64"
$env:Path = "$nodeRoot;$env:Path"
npm run build
```

## Environment

Frontend environment values belong in:

```text
frontend/.env.local
```

Typical value:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

For local development:

```text
Frontend: http://127.0.0.1:3000
Backend:  http://127.0.0.1:8000
```

## Notes

- Do not commit real secrets.
- Do not commit `node_modules`.
- Do not commit `.next`.
- Dashboard pages should gracefully handle missing or partial backend data.
