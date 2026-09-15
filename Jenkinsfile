pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright:v1.62.1-jammy'
            args '-u root'
        }
    }

    options {
        timestamps()
    }

    stages {
        stage('Install Python dependencies') {
            steps {
                sh 'apt-get update && apt-get install -y python3-pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh 'python3 -m pytest tests/test_login.py -v --junitxml=results/junit.xml'
            }
        }
    }

    post {
        always {
            junit 'results/junit.xml'
        }
    }
}