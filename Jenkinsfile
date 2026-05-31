pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/VirajChauhan02/UIDAI-Biometric-Analytics-Dashboard.git'
            }
        }

        stage('Bandit Scan') {
            steps {
                bat 'pip install bandit'
                bat 'bandit -r .'
            }
        }

        stage('Gitleaks Scan') {
            steps {
                bat 'echo Gitleaks Scan Stage'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                bat 'echo SonarQube Analysis Stage'
            }
        }
    }
}