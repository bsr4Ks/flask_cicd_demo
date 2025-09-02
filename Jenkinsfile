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


        stage('Push to Harbor') {

            when {
                expression {
                    return env.BRANCH_NAME == "dep-harbor"
                } 
            }

            steps {
                withCredentials([usernamePassword(credentialsId: 'basaraksu-harbor', usernameVariable: 'HARBOR_USER', passwordVariable: 'HARBOR_PASS')]) {
                    sh """
                        echo \$HARBOR_PASS | docker login harbor.local -u \$HARBOR_USER --password-stdin
                        docker tag ${IMAGE_NAME}:latest harbor.local/devops-test/${IMAGE_NAME}:latest
                        docker push harbor.local/devops-test/${IMAGE_NAME}:latest
                        docker logout harbor.local
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
