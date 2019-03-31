FROM redis:4.0

COPY ./redis-secondary.conf /etc/redis/redis.conf
CMD ["redis-server", "/etc/redis/redis.conf"]