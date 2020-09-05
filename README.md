docker build --rm -f "dash-docker\Dockerfile" -t dash_test_w "dash-docker"
docker run -d -it -p 8080:8080 dash_test_w