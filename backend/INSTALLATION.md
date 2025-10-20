# Quick Installation Guide

## For Linux Pop!_OS

### 1. Install Prerequisites

\`\`\`bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Verify installations
python3 --version
node --version
npm --version
\`\`\`

### 2. Setup Neo4j Aura

1. Visit https://neo4j.com/cloud/aura/
2. Sign up for free account
3. Create new AuraDB Free instance
4. Save credentials (URI, username, password)

### 3. Setup Project

\`\`\`bash
# Extract and navigate
unzip boardinghouse-system.zip
cd boardinghouse-system

# Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Neo4j credentials
nano .env

# Setup Frontend (in new terminal)
cd frontend
npm install
\`\`\`

### 4. Run Application

**Terminal 1 - Backend:**
\`\`\`bash
cd backend
source venv/bin/activate
python main.py
\`\`\`

**Terminal 2 - Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

### 5. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

### 6. Create First Admin User

1. Go to http://localhost:3000/register
2. Fill in details and select "Admin" role
3. Login and start managing the system

## Quick Test

1. Login as admin
2. Create a room (Rooms tab)
3. Logout and register as user
4. Login as user and book the room
5. Logout and login as admin
6. Approve the booking (Notifications tab)

Done! The system is ready to use.
