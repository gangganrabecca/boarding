# Boardinghouse Management System

A complete full-stack boardinghouse management system with FastAPI backend, React frontend, and Neo4j Aura database.

## Features

### User Features
- User registration and login with JWT authentication
- **Browse available rooms** before booking
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

### Step 5: Run the Application (Alternative - Mock Backend)

If you don't have access to Neo4j Aura or want to test without the database:

#### Terminal 1 - Start Mock Backend (No Database Required):
```bash
cd backend
python minimal_app.py
```

#### Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```

**Note:** The mock backend provides full API functionality with sample data, perfect for testing and development without database setup.

### Step 6: Test Connectivity
```bash
./test_connectivity.sh
```

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

**Or use the pre-created accounts:**

**Admin Account (Fixed Credentials):**
- Email: admin@boardinghouse.com
- Password: admin123

**Note:** The admin account is automatically created when the backend starts up using the credentials from the `.env` file.

## 📱 Mobile Responsiveness Features

The application is fully optimized for mobile devices with:

### 🎯 Mobile-First Design
- **Responsive Navigation**: Hamburger menu with smooth animations
- **Touch-Friendly Interface**: 44px minimum touch targets for all interactive elements
- **Adaptive Layouts**: Grid systems that stack properly on mobile devices
- **Mobile Typography**: Responsive text sizes for optimal readability
- **Touch Scrolling**: Smooth scrolling with proper overflow handling

### 📐 Responsive Breakpoints
- **Mobile**: < 640px (sm) - Single column layouts, stacked navigation
- **Tablet**: 640px - 1024px (md/lg) - Two column layouts, condensed navigation
- **Desktop**: > 1024px (xl) - Full multi-column layouts

### ✨ Mobile Features Added
- ✅ Overview dashboard moved below tab navigation (as requested)
- ✅ Responsive dashboard statistics with mobile-optimized cards
- ✅ Mobile-friendly forms with proper field stacking
- ✅ Touch-optimized buttons and navigation elements
- ✅ Responsive data tables and information displays
- ✅ Mobile-optimized loading states and error messages

### 🧪 Mobile Testing
1. Open http://localhost:3000 in your browser
2. Use browser dev tools (F12) to simulate mobile devices
3. Test on actual mobile devices for best experience
4. Run `./test_connectivity.sh` to verify all endpoints work correctly

## How It Works

### Role-Based Access Control

The system uses JWT tokens with role information to control access:

- **Admin users** (role: "admin") are automatically redirected to `/admin` dashboard
- **Regular users** (role: "user") are automatically redirected to `/dashboard`
- **Unauthenticated users** are redirected to the login page

### Automatic Dashboard Routing

After successful login, the system automatically determines the user's role and redirects them to the appropriate dashboard:

1. **Admin Login** → Redirects to Admin Dashboard (`/admin`)
   - Can manage rooms, tenants, and approve bookings
   - Full system access

2. **User Login** → Redirects to User Dashboard (`/dashboard`)
   - Can browse available rooms and create bookings
   - Can view and manage personal bookings
   - Receives notifications about booking status

### Notification System

- When users create bookings, notifications are automatically created
- Admins can see all booking requests in the Admin Dashboard
- Admins can approve or reject bookings with one click
- Users receive notifications when their bookings are approved/rejected
- Room status automatically updates when bookings are approved

### Enhanced Admin Workflow

1. **Dashboard Overview**: Start with the Overview tab to see system statistics at a glance
2. **Room Management**: Navigate to "Rooms" tab to create and manage room inventory
3. **Tenant Management**: Use "Tenants" tab to add and manage tenant information
4. **Booking Approvals**: Check "Notifications" tab for pending booking requests
5. **Quick Actions**: Click "Book Now" on any room to pre-fill booking forms for users

### Enhanced User Workflow

1. **Personal Dashboard**: Overview tab shows your booking statistics and system status
2. **Room Discovery**: Browse available rooms with filtering options in "Available Rooms" tab
3. **Smart Booking**: Click "Book Now" on any room to auto-fill the booking form
4. **Easy Booking**: Use the enhanced booking form with auto-duration calculation
5. **Booking Management**: View and manage all your bookings in "My Bookings" tab
6. **Status Updates**: Check "Notifications" tab for booking approval updates

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
│   │   │   ├── DashboardOverview.jsx    # Dashboard statistics component
│   │   │   ├── AdminNotifications.jsx  # Admin booking notifications
│   │   │   ├── AvailableRooms.jsx       # Room browsing with filters
│   │   │   ├── BookingForm.jsx          # Enhanced booking form
│   │   │   ├── MyBookings.jsx           # User booking management
│   │   │   ├── RoomsList.jsx            # Admin room management
│   │   │   ├── TenantsList.jsx          # Admin tenant management
│   │   │   ├── UserNotifications.jsx    # User notifications
│   │   │   └── Navbar.jsx               # Navigation component
│   │   ├── pages/           # Page components
│   │   │   ├── AdminDashboard.jsx       # Admin dashboard with overview
│   │   │   ├── UserDashboard.jsx        # User dashboard with overview
│   │   │   ├── Login.jsx                # Login page
│   │   │   └── Register.jsx             # Registration page
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

## Enhanced Features

### 📊 Dashboard Overview
- **Real-time Statistics**: Both admin and user dashboards now display comprehensive statistics
- **Admin Overview**: Total rooms, available rooms, occupied rooms, and tenant count
- **User Overview**: Personal booking statistics, pending/approved bookings, and available rooms
- **Visual Cards**: Beautiful metric cards with icons and color-coded information

### 🏠 Enhanced Room Management
- **Room Filtering**: Filter available rooms by type (Single, Double, Suite)
- **Room Pre-selection**: Click "Book Now" on any room to automatically pre-fill the booking form
- **Enhanced UI**: Improved room cards with hover effects and better visual hierarchy
- **Real-time Updates**: Room availability updates immediately after booking approval

### 📝 Smart Booking System
- **Auto-Duration Calculation**: Booking duration automatically calculated from selected dates
- **Date Validation**: Prevents booking end dates before start dates
- **Pre-filled Forms**: Room selection from Available Rooms tab auto-fills the booking form
- **Success Callbacks**: Seamless navigation after successful booking creation

### 📋 Enhanced Booking Management
- **Detailed Booking Cards**: Comprehensive booking information with total pricing
- **Status Management**: Clear visual indicators for pending, approved, rejected, and cancelled bookings
- **Easy Cancellation**: One-click cancellation for pending bookings with confirmation
- **Better Error Handling**: Toast notifications and loading states throughout

### 🔔 Improved Notifications
- **Enhanced Admin Notifications**: Better styling, loading states, and error handling
- **User Notifications**: Personal booking status updates and system notifications
- **Real-time Updates**: Automatic refresh after status changes
- **Visual Status Indicators**: Color-coded badges and status information

### 🎨 UI/UX Improvements
- **Responsive Design**: Optimized for all screen sizes
- **Loading States**: Skeleton loading and spinners throughout the application
- **Error Handling**: Comprehensive error messages and retry mechanisms
- **Smooth Animations**: Hover effects, transitions, and micro-interactions
- **Consistent Styling**: Unified design system with Tailwind CSS

- Payment integration
- Email notifications
- Room availability calendar
- Advanced search and filtering
- Tenant payment tracking
- Maintenance request system
- File upload for documents
- Reports and analytics
# bex
