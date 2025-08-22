pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myapp'
        CONTAINER_NAME = 'myapp-c'
        PORT = '5000'
    }

    stages {

        stage ('Example') {
            steps {
                echo 'Jenkins starts!'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Container') {
            steps {
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -d ${IMAGE_NAME}
                """
            }
        }
        stage('Push to Docker Hub') {
            steps {

            sh """
                echo ${IMAGE_NAME}
                docker tag ${IMAGE_NAME} $DOCKER_USER/flask-app:latest
            """


            docker.withRegistry('https://registry.hub.docker.com', 'basaraksu-dockerhub') {            
                sh """
                    docker push $DOCKER_USER/flask-app:latest
                """
            }

            // withCredentials([usernamePassword(credentialsId: "basaraksu-dockerhub")]) {
            //     sh """
            //         # echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            //         docker tag ${IMAGE_NAME} $DOCKER_USER/flask-app:latest
            //         docker push $DOCKER_USER/flask-app:latest
            //         """
            // }
        }
}   

    }
}
