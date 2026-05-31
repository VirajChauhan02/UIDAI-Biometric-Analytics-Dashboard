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
                withSonarQubeEnv('SonarQube') {

                    bat """
                    C:\\Users\\HP\\Downloads\\sonarqube-26.5.0.122743\\sonar-scanner-cli-8.0.1.6346-windows-x64\\sonar-scanner-8.0.1.6346-windows-x64\\bin\\sonar-scanner.bat ^
                    -Dsonar.projectKey=UIDAI-Biometric-Analytics ^
                    -Dsonar.projectName=UIDAI-Biometric-Analytics ^
                    -Dsonar.sources=. ^
                    -Dsonar.host.url=http://localhost:9000
                    """
                }
            }
        }
    }
}