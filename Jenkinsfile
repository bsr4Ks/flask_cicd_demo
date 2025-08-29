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
                sh "python3 -m venv venv"
                sh "venv/bin/pip3 install -r requirements.txt"
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
                        docker tag ${IMAGE_NAME} $DOCKER_USER/flask-app:latest
                        docker push $DOCKER_USER/flask-app:latest
                    """
                }
            }
        }

        stage('Push Tagged Release to Docker Hub') {
            when {
                buildingTag()
            }
            environment {
                DOCKER_IMAGE = "bsr4ks/flask-cicd-demo"
                TAG_NAME = "${env.GIT_TAG_NAME ?: 'latest'}"
            }
            steps {
                script {
                    echo "🔖 Building Docker image for tag: ${TAG_NAME}"

                    // Build image with tag
                    sh "docker build -t ${DOCKER_IMAGE}:${TAG_NAME} ."

                    // Check if tag already exists on Docker Hub
                    def tagExists = sh(
                        script: "curl -s https://hub.docker.com/v2/repositories/${DOCKER_IMAGE}/tags/${TAG_NAME} | grep -q 'name'",
                        returnStatus: true
                    ) == 0

                    if (tagExists) {
                        error "❌ Docker tag '${TAG_NAME}' already exists on Docker Hub. Aborting to avoid overwrite."
                    }   

                    // Push image
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                    echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                    docker push ${DOCKER_IMAGE}:${TAG_NAME}
                    docker logout
                    """
                }

                echo "✅ Docker image ${DOCKER_IMAGE}:${TAG_NAME} pushed successfully."
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
