FROM nginx:1.27-alpine

# Gradient Path is a fully static site -- no build step. Every HTML file here
# is a finished, generated artifact (01-linear-algebra, 03-machine-learning and
# 04-llms are generator output, not hand-edited source -- see project notes).
# The wildcard copy means a new module only needs an index.html update and a
# git push -- nothing here has to change.
COPY nginx.conf /etc/nginx/nginx.conf
COPY *.html /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -q --spider http://localhost/healthz || exit 1
