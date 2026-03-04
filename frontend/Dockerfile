# Use the lightweight Nginx alpine image
FROM nginx:alpine

# Copy the frontend files to the Nginx default public directory
COPY index.html /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Expose port 80 for web traffic
EXPOSE 80

# Nginx starts automatically, no CMD needed