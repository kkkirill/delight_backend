# delight

## Online audio distribution platform and music sharing website


Installation Docker and its dependencies:
1) [Install Docker][1]
2) [Install Docker Compose][2]

Build container:
1) Enter project folder.
    ```bash
    cd delight
    # (you should get to the same level with Dockerfile)
    ```
2) Build container.
    ```bash
    docker-compose build
    ```

    Note:<br>
    To update pip dependencies, run Django model migrations and start server execute following:
    ```bash
    docker-compose -f docker-compose.yaml -f docker-compose.setup.yaml up
    ```
    To make migrations and apply them run following:
    ```bash
    docker-compose -f docker-compose.yaml -f docker-compose.mkmigrations.yaml up
    ```
    To show running containers run following:
    ```bash
    docker[-compose] ps
    ```
    To stop running containers run following:
    ```bash
    docker-compose stop
    ```

3) Before run container run following:
   <br>Install AWS CLI:
   ```bash
   sudo apt install awscli 
   ```
   <br>Create AWS bucker:
   ```bash
   aws --endpoint-url=http://0.0.0.0:4572 s3 mb s3://delight-media
   ```
   <br>Add bucket ACL:
   ```bash
   aws --endpoint-url=http://0.0.0.0:4572 s3api put-bucket-acl --bucket delight-media --acl public-read
   ```

4) Run container.
    ```bash
    docker-compose up
    ```
    ```bash
    docker-compose start
    ```

[1]: https://docs.docker.com/install/linux/docker-ce/ubuntu/
[2]: https://docs.docker.com/compose/install/
