pipeline {
    agent any

    tools {
        sonarQube 'SonarScanner' // Must match the name in Jenkins > Global Tool Configuration
    }

    environment {
        IMAGE_NAME = 'myapp-i'
        CONTAINER_NAME = 'myapp-c'
        PORT = '5000'
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Start') {
            steps {
                echo 'Jenkins starts!'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') { // Must match Jenkins > SonarQube server name
                    sh "${SCANNER_HOME}/bin/sonar-scanner"
                }
            }
        }

        stage('Cleanup Container') {
            steps {
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker rmi ${IMAGE_NAME} || true
                    docker build -t ${IMAGE_NAME} .
                """
            }
        }

        stage('Run Container') {
            steps {
                sh """
                    docker run --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -d ${IMAGE_NAME}
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'basaraksu-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        docker tag ${IMAGE_NAME} $DOCKER_USER/flask-app:latest
                        docker push $DOCKER_USER/flask-app:latest
                    """
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Pipeline failed. No deployment triggered.'
        }
        success {
            echo '✅ Pipeline succeeded. Deployment completed.'
        }
    }
}
