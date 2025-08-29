pipeline {
    agent any

    environment {
        IMAGE_NAME = "basaraksu/flask-app"
        CONTAINER_NAME = 'basaraksu_flask-app_c'
        PORT = '5000'
    }

    stages {
        stage('Start') {
            steps {
                echo 'Jenkins starts!'
                sh "python3 -m venv venv"
                sh "venv/bin/pip3 install -r requirements.txt"
                sh "echo $env.GIT_TAG_NAME"
            }
        }

        stage('Info') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
            }
        }

        stage('SonarQube Analysis') {

            when {
                expression {
                    return env.BRANCH_NAME == "dev" || env.BRANCH_NAME ==~ /^feature\/.+/
                } 
            }

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

            when {
                expression {
                    return env.BRANCH_NAME == "dev" || env.BRANCH_NAME ==~ /^feature\/.+/
                } 
            }

            steps {
            sh """
            ./venv/bin/pytest tests/ --junitxml=report.xml
            """
        }
        }
        stage('Cleanup Container') {

            when {
                expression {
                    return env.BRANCH_NAME == "dev"
                } 
            }


            steps {
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Build Docker Image') {

            when {
                expression {
                    return env.BRANCH_NAME == "dev"
                } 
            }

            steps {
                sh """
                    docker rmi ${IMAGE_NAME} || true
                    docker build -t ${IMAGE_NAME} .
                """
            }
        }

        stage('Run Container') {

            when {
                expression {
                    return env.BRANCH_NAME == "dev"
                } 
            }

            steps {
                sh """
                    docker run --name ${CONTAINER_NAME} -p ${PORT}:${PORT} -d ${IMAGE_NAME}
                """
            }
        }

        stage('Push to Docker Hub') {

            when {
                expression {
                    return env.BRANCH_NAME == "main" || env.BRANCH_NAME == "deploy"
                } 
            }

            steps {
                withCredentials([usernamePassword(credentialsId: 'basaraksu-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        docker push ${IMAGE_NAME}
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
