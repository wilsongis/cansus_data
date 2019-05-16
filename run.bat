
docker build -t census_data -f config/census_data.Dockerfile .
docker run --privileged -ti -v ${PWD}:/usr/local/bin/census_data -p 8888:8888 census_data