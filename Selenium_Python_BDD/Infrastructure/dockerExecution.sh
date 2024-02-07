docker network create grid
docker run -d -p 4442-4444:4442-4444 --net grid --name selenium-hub selenium/hub:4.0.0-beta-4-prerelease-20210527
docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_NODE_MAX_SESSIONS=6 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    -v /dev/shm:/dev/shm \
    -p 5900:5900 \
    selenium/node-chrome:4.0.0-beta-4-prerelease-20210527
docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_NODE_MAX_SESSIONS=6 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    -v /dev/shm:/dev/shm \
    -p 5901:5900 \
    selenium/node-edge:4.0.0-beta-4-prerelease-20210527
docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_NODE_MAX_SESSIONS=6 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    -v /dev/shm:/dev/shm \
    -p 5902:5900 \
    selenium/node-firefox:4.0.0-beta-4-prerelease-20210527
docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_NODE_MAX_SESSIONS=6 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    -v /dev/shm:/dev/shm \
    -p 5903:5900 \
    selenium/node-opera:4

export LOAD_BALANCER_NAME=http://localhost:4444
export BROWSER_NAME=chrome