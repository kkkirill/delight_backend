# delight

## Online audio distribution platform and music sharing website


Installation Docker and its dependencies:
1) [Install Docker][1]
2) [Install Docker Compose][2]

Quick start:
1) Enter project folder.
    ```bash
    cd delight
    # (you should get to the same level with Dockerfile)
    ```
2) Run server.
    ```bash
    sudo docker-compose up -d --build
    ```

    Note:<br>
    To show running containers run following:
    ```bash
    sudo docker ps
    ```
    To stop running containers run following:
    ```bash
    sudo docker-compose stop
    ```

Run tests:

1) Install `make`.

    ```bash
    sudo apt-get install build-essential 
    ```
2) Run tests.

    ```bash
    sudo make test
    ```


[1]: https://docs.docker.com/install/linux/docker-ce/ubuntu/
[2]: https://docs.docker.com/compose/install/
