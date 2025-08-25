pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myapp-i'
        CONTAINER_NAME = 'myapp-c'
        PORT = '5000'
    }

    stages {

        stage ('Example') {
            steps {
                echo 'Jenkins starts!'
            }
        }

        stage('SonarQube Analysis') {
            def scannerHome = tool 'SonarScanner';
            withSonarQubeEnv('sonarqube') {
            sh "${scannerHome}/bin/sonar-scanner"
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

            sh """
            echo ${IMAGE_NAME}
            """

            withCredentials([usernamePassword(credentialsId: 'basaraksu-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                sh 'echo $DOCKER_USER'
                sh """
                    docker tag ${IMAGE_NAME} $DOCKER_USER/flask-app:latest
                    docker push $DOCKER_USER/flask-app:latest
                    """
            }
        }
    }   
        post {
            failure {
                echo 'Pipeline failed. No deployment triggered.'
            }
            success {
                echo 'Pipeline succeeded. Deployment completed.'
            }
    }

    }
}
