# Deployment Environment Variables

## Backend Environment Variables (for Render)

The following environment variables need to be set in your Render backend service:

### Required Variables:
- `NEO4J_URI`: Your Neo4j Aura database URI (format: `neo4j+s://xxxxxxxx.databases.neo4j.io`)
- `NEO4J_USERNAME`: Your Neo4j Aura username (usually `neo4j`)
- `NEO4J_PASSWORD`: Your Neo4j Aura password

### Frontend Environment Variables (for Render)

The following environment variable needs to be set in your Render frontend service:

- `VITE_API_URL`: URL of your backend service (format: `https://your-backend-service-name.onrender.com/api`)

## Setting up Environment Variables in Render:

1. In your Render dashboard, go to your service settings
2. Navigate to "Environment" section
3. Add each variable with its corresponding value
4. Redeploy the service for changes to take effect

## Example Values:
- NEO4J_URI: `neo4j+s://abc123def456.databases.neo4j.io`
- NEO4J_USERNAME: `neo4j`
- NEO4J_PASSWORD: `your-actual-password-here`
- VITE_API_URL: `https://your-backend-service.onrender.com/api`
