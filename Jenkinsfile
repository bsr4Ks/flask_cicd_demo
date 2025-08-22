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

        stage('Deploy Container') {
            steps {
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -d ${IMAGE_NAME}
                """
            }
        }
    }
}
