# Use a lightweight web server
FROM nginx:alpine

# Copy our HTML, CSS, and JS files to the web server directory
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Expose port 80 for the web server
EXPOSE 80

# Nginx starts automatically by default
