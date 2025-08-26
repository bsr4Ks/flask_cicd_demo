pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myapp-i'
        CONTAINER_NAME = 'myapp-c'
        PORT = '5000'
    }

    stages {
        stage('Start') {
            steps {
                echo 'Jenkins starts!'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv('sonarqube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Test') {
            steps {
            sh "pytest tests/ --junitxml=report.xml"
            junit 'report.xml'
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
