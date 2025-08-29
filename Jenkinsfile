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

        stage('release') {
            steps {
                sh """
                    echo here!
                """
            }
        }
        
        stage('Push tagged release to Dockerhub') {
            when {
                buildingTag()
            }
            
            steps {
                script {
                    def tag = sh(script: "git describe --tags --exact-match || echo ''", returnStdout: true).trim()
                    echo "Detected tag: ${tag}"
                
                    // Build image with tag
                    sh """docker build -t ${IMAGE_NAME}:${tag} ."""

                    // Check if tag already exists on Docker Hub
                    // ?? 

                    // Push image
                    withCredentials([usernamePassword(credentialsId: 'basaraksu-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            # echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                            docker push ${DOCKER_IMAGE}:${tag}
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
