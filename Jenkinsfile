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
                sh "echo ansible --version"
                sh "echo ansible-playbook --version" 
            }
        }

        stage('Info') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
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
