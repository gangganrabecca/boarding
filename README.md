# Boardinghouse Management System

A complete full-stack boardinghouse management system with FastAPI backend, React frontend, and Neo4j Aura database.

## Features

### User Features
- User registration and login with JWT authentication
- Book rooms with date selection and duration
- View and manage personal bookings
- Cancel pending bookings
- Receive notifications about booking status

### Admin Features
- Manage tenants (add, view tenant information)
- Manage rooms (create, view, delete rooms)
- Review and approve/reject booking requests
- View all notifications and booking requests
- Update room status (available, occupied, maintenance)

## Technology Stack

### Backend
- FastAPI (Python web framework)
- Neo4j Aura (Graph database)
- JWT authentication
- Pydantic for data validation
- Uvicorn ASGI server

### Frontend
- React 18
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- Vite for build tooling

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Neo4j Aura account (free tier available at https://neo4j.com/cloud/aura/)

## Installation Instructions for Linux Pop!_OS

### Step 1: Extract the ZIP file

\`\`\`bash
unzip boardinghouse-system.zip
cd boardinghouse-system
\`\`\`

### Step 2: Setup Neo4j Aura Database

1. Go to https://neo4j.com/cloud/aura/ and create a free account
2. Create a new AuraDB Free instance
3. Save the connection URI, username, and password provided
4. Wait for the instance to be ready (usually takes 1-2 minutes)

### Step 3: Setup Backend

\`\`\`bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env file with your Neo4j credentials
nano .env
\`\`\`

Update the `.env` file with your Neo4j Aura credentials:

\`\`\`env
NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-from-aura

JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

PORT=8000
\`\`\`

Save and exit (Ctrl+X, then Y, then Enter).

### Step 4: Setup Frontend

Open a new terminal window:

\`\`\`bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# The frontend is configured to proxy API requests to http://localhost:8000
# No additional configuration needed
\`\`\`

### Step 5: Run the Application

#### Terminal 1 - Start Backend:

\`\`\`bash
cd backend
source venv/bin/activate
python main.py
\`\`\`

The backend will start on http://localhost:8000

#### Terminal 2 - Start Frontend:

\`\`\`bash
cd frontend
npm run dev
\`\`\`

The frontend will start on http://localhost:3000

### Step 6: Access the Application

Open your browser and navigate to:
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

### Step 7: Create Initial Users

1. Go to http://localhost:3000/register
2. Create an admin account:
   - Email: admin@example.com
   - Username: admin
   - Password: admin123
   - Role: Admin

3. Create a user account:
   - Email: user@example.com
   - Username: user
   - Password: user123
   - Role: User

## Usage Guide

### Admin Workflow

1. Login with admin credentials
2. Navigate to "Rooms" tab
3. Click "Add Room" to create rooms:
   - Room Number: 101
   - Room Type: Single
   - Capacity: 1
   - Price: 500
   - Status: Available

4. Navigate to "Tenants" tab to add tenant information
5. Navigate to "Notifications" tab to review and approve/reject booking requests

### User Workflow

1. Login with user credentials
2. Navigate to "Booking" tab
3. Select an available room
4. Choose start date, end date, and duration
5. Submit booking request
6. Navigate to "My Bookings" to view booking status
7. Navigate to "Notifications" to see approval status

## Project Structure

\`\`\`
boardinghouse-system/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Neo4j database operations
│   ├── models.py            # Pydantic models
│   ├── auth.py              # JWT authentication logic
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── .env                 # Your environment variables (create this)
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── context/         # React context (Auth)
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── tailwind.config.js   # Tailwind CSS configuration
│
└── README.md                # This file
\`\`\`

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- GET `/api/auth/me` - Get current user

### Bookings
- POST `/api/bookings` - Create booking (User)
- GET `/api/bookings/my` - Get user's bookings (User)
- PUT `/api/bookings/{id}` - Update booking (User)
- DELETE `/api/bookings/{id}` - Cancel booking (User)

### Rooms
- GET `/api/rooms` - Get all rooms
- GET `/api/rooms/{id}` - Get room by ID
- POST `/api/rooms` - Create room (Admin)
- PUT `/api/rooms/{id}` - Update room (Admin)
- DELETE `/api/rooms/{id}` - Delete room (Admin)

### Tenants
- GET `/api/tenants` - Get all tenants (Admin)
- POST `/api/tenants` - Create tenant (Admin)

### Notifications
- GET `/api/notifications` - Get notifications
- PUT `/api/notifications/{id}` - Update notification (Admin)

## Troubleshooting

### Backend Issues

**Error: "Could not connect to Neo4j"**
- Verify your Neo4j Aura instance is running
- Check that the URI, username, and password in `.env` are correct
- Ensure the URI starts with `neo4j+s://` for Aura

**Error: "Module not found"**
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Error: "Cannot connect to backend"**
- Ensure the backend is running on port 8000
- Check that the proxy configuration in `vite.config.js` is correct

**Error: "npm install fails"**
- Try clearing npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then run `npm install` again

### Database Issues

**Error: "Constraint already exists"**
- This is normal on subsequent runs, the app will continue to work

**Need to reset database**
- Go to Neo4j Aura console
- Delete all nodes: Run `MATCH (n) DETACH DELETE n` in the query browser

## Development

### Backend Development

\`\`\`bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

### Frontend Development

\`\`\`bash
cd frontend

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
\`\`\`

## Security Notes

- Change the `JWT_SECRET_KEY` in production
- Use strong passwords for Neo4j Aura
- Never commit `.env` file to version control
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Add input validation and sanitization

## License

MIT License - Feel free to use this project for learning and development.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the Neo4j Aura documentation
3. Check FastAPI documentation at https://fastapi.tiangolo.com
4. Check React documentation at https://react.dev

## Future Enhancements

- Payment integration
- Email notifications
- Room availability calendar
- Advanced search and filtering
- Tenant payment tracking
- Maintenance request system
- File upload for documents
- Reports and analytics
