# Frontend – ATS Project (React + Vite)

This is the **frontend** of the ATS (Applicant Tracking System) project.  
It’s built with **React (JSX)** and **Vite**, providing a fast, modern development setup for building dynamic and responsive interfaces.

---

## 🧱 Tech Stack

- **React** (JSX)
- **Vite** (development/build tool)
- **React Router DOM** – for routing between pages
- **Axios** – for API calls
- **Django REST Framework backend** (connected at `http://127.0.0.1:8000/api`)

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/eytahnlouis/ats-project.git
   cd ats-project/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to the URL displayed in the terminal (usually `http://localhost:5173/`).

---

## 🔗 Backend Connection

The frontend communicates with the Django backend using the `/api` endpoints:
- `api/cvs/jobs/` – get list of job offers  
- `api/cvs/upload/` – upload candidate resume  
- `api/cvs/my-candidates/` – view user submissions  

Make sure your **Django backend** is running before launching the frontend:
```bash
cd ../backend
python manage.py runserver
```

---

## 🧩 Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page-level components (Jobs, Upload, etc.)
│   ├── assets/            # Images, icons, styles
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # Entry point
├── index.html
├── package.json
└── vite.config.js
```

---

## 🧠 Development Notes

- Uses **React Router** for page navigation (`onClick` → `navigate('/upload')` etc.)
- API requests are handled via **Axios** and can include auth tokens if needed.
- Backend CORS should be properly configured to allow frontend requests from `localhost:5173`.

---

## 🚀 Build for Production

To create an optimized production build:
```bash
npm run build
```

This generates a `/dist` folder ready for deployment.

---

## 💡 Next Steps

- Create admin dashboard
- Add form validation and user feedback
- Improve styling and responsiveness

---

Made with ❤️ using React + Vite.
 